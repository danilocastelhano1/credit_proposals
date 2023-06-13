from rest_framework import serializers

from digitalsys.api.models import CreditProposal


class CreditProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditProposal
        fields = (
            "id", "fullname", "cpf", "address", "proposal_value", "status", "created_at", "updated_at"
        )
        read_only_fields = ("status", "created_at", "updated_at")
