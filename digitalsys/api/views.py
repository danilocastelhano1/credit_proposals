import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from digitalsys.api.models import CreditProposal
from digitalsys.api.serializers import CreditProposalSerializer


class CreditProposalViewSet(ModelViewSet):
    queryset = CreditProposal.objects.all()
    serializer_class = CreditProposalSerializer
    permission_classes = [AllowAny]


def index(request):
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
