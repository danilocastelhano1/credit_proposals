from rest_framework import serializers

from digitalsys.api.models import CreditProposal
from digitalsys.api.models import Proposal
from digitalsys.api.models import ProposalFieldsValue


class CreditProposalSerializer(serializers.ModelSerializer):
    """
    OLD we don't use anymore
    """

    class Meta:
        model = CreditProposal
        fields = (
            "id",
            "fullname",
            "cpf",
            "address",
            "proposal_value",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status", "created_at", "updated_at")


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = (
            "id",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status", "created_at", "updated_at")


class ProposalFieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalFieldsValue
        fields = (
            "id",
            "field",
            "proposal",
            "field_value",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status", "created_at", "updated_at")
