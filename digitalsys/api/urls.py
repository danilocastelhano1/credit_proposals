from django.urls import include
from django.urls import path
from rest_framework import routers

from digitalsys.api.views import CreditProposalViewSet
from digitalsys.api.views import ProposalFieldValueViewSet
from digitalsys.api.views import ProposalViewSet
from digitalsys.api.views import index

router = routers.DefaultRouter()
router.register(
    r"credit_proposal", CreditProposalViewSet, basename="credit_proposal"
)  # OLD Way
router.register(r"proposal", ProposalViewSet, basename="proposal")
router.register(
    r"proposal_field_value", ProposalFieldValueViewSet, basename="proposal_field_value"
)


urlpatterns = [
    path(r"", index, name="index"),
    path(r"api/", include(router.urls)),
]
