import logging
import math

from typing import List

from celery import shared_task
from django.utils import timezone

from digitalsys.api.models import CreditProposal

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def change_status(self):
    credit_proposals = CreditProposal.objects.filter(
        status=CreditProposal.CreditChoices.PENDING
    ).all()

    if credit_proposals:
        credit_proposals_to_be_updated: List[CreditProposal] = []

        logger.info("Got %s records to be updated", credit_proposals.count())
        floor: int = math.floor(credit_proposals.count() / 2)
        count: int = 0
        for credit_proposal in credit_proposals:
            count += 1
            if count <= floor:
                credit_proposal.status = CreditProposal.CreditChoices.DENIED
            else:
                credit_proposal.status = CreditProposal.CreditChoices.APPROVED

            credit_proposal.updated_at = timezone.now()
            credit_proposals_to_be_updated.append(credit_proposal)

        CreditProposal.objects.bulk_update(
            credit_proposals_to_be_updated, ["status", "updated_at"]
        )
        logger.info("Task ended with successfully")
    else:
        logger.info("No credit proposals to be updated, all good")
    return "Success"
