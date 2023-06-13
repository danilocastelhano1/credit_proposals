from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from digitalsys.api.models import CreditProposal

from digitalsys.api.serializers import CreditProposalSerializer

# Create your views here.


class CreditProposalViewSet(ModelViewSet):
    queryset = CreditProposal.objects.all()
    serializer_class = CreditProposalSerializer
    permission_classes = [AllowAny]
