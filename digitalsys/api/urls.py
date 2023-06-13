from django.urls import include, path
from rest_framework import routers

from digitalsys.api.views import CreditProposalViewSet

router = routers.DefaultRouter()
router.register(r"credit_proposal", CreditProposalViewSet)

urlpatterns = [
    path(r"api/", include(router.urls)),
]
