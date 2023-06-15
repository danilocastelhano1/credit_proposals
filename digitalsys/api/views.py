from http import HTTPStatus
from typing import Dict
from typing import List

import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from digitalsys.api.models import CreditProposal
from digitalsys.api.models import Proposal
from digitalsys.api.models import ProposalFields
from digitalsys.api.models import ProposalFieldsValue
from digitalsys.api.serializers import CreditProposalSerializer
from digitalsys.api.serializers import ProposalFieldValueSerializer
from digitalsys.api.serializers import ProposalSerializer


class CreditProposalViewSet(ModelViewSet):
    """
    OLD we don't use anymore
    """

    queryset = CreditProposal.objects.all()
    serializer_class = CreditProposalSerializer
    permission_classes = [AllowAny]


class ProposalViewSet(ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [AllowAny]


class ProposalFieldValueViewSet(ModelViewSet):
    queryset = ProposalFieldsValue.objects.all()
    serializer_class = ProposalFieldValueSerializer
    permission_classes = [AllowAny]


def old_index(request):
    """
    List all Credit Proposals and stores into database if POST is called
    """
    if request.method == "GET":
        jobs = CreditProposal.objects.all()
        return render(request, "index.html", {"credit_proposals": jobs})
    elif request.method == "POST":
        data = {
            "fullname": request.POST["fullname"],
            "cpf": request.POST["cpf"],
            "address": request.POST["address"],
            "proposal_value": request.POST["proposal_value"],
        }

        # Call internal API
        path_url = reverse("credit_proposal-list")
        requests.post(request.headers.get("Origin") + path_url, data=data)

        return HttpResponseRedirect("/")


def index(request):
    """
    List all Credit Proposals and stores into database if POST is called
    """
    proposals_field_names: List = []

    proposal_fields = ProposalFields.objects.all()
    for proposal_field in proposal_fields:
        proposals_field_names.append(proposal_field.field_name)

    if request.method == "GET":
        proposals = Proposal.objects.all()

        return render(
            request,
            "index.html",
            {"credit_proposals": proposals, "proposal_fields": proposal_fields},
        )
    elif request.method == "POST":
        data: Dict = {}

        for key, value in request.POST.items():
            if key in proposals_field_names:
                data[key] = value

        # Call internal API
        proposal_url = reverse("proposal-list")
        proposal_field_value_url = reverse("proposal_field_value-list")

        # Create a new Proposal
        proposal_response = requests.post(request.headers.get("Origin") + proposal_url)
        if proposal_response.status_code != HTTPStatus.CREATED:
            return

        for field_key, field_value in data.items():
            body: Dict = {
                "field": ProposalFields.objects.filter(field_name=field_key).get().id,
                "proposal": proposal_response.json()["id"],
                "field_value": field_value,
            }
            requests.post(
                request.headers.get("Origin") + proposal_field_value_url, data=body
            )

        return HttpResponseRedirect("/")
