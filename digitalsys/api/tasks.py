import logging
import math

from typing import List

from celery import shared_task
from django.utils import timezone

from digitalsys.api.models import CreditChoices
from digitalsys.api.models import Proposal

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def change_status(self):
    proposals = Proposal.objects.filter(status=CreditChoices.PENDING).all()

    if proposals:
        proposals_to_be_updated: List[Proposal] = []

        logger.info("Got %s records to be updated", proposals.count())
        floor: int = math.floor(proposals.count() / 2)
        count: int = 0
        for proposal in proposals:
            count += 1
            if count <= floor:
                proposal.status = CreditChoices.DENIED
            else:
                proposal.status = CreditChoices.APPROVED

            proposal.updated_at = timezone.now()
            proposals_to_be_updated.append(proposal)

        Proposal.objects.bulk_update(proposals_to_be_updated, ["status", "updated_at"])
        logger.info("Task ended with successfully")
    else:
        logger.info("No credit proposals to be updated, all good")
    return "Success"
