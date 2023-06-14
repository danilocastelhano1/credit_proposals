from django.urls import include
from django.urls import path
from rest_framework import routers

from digitalsys.api.views import CreditProposalViewSet
from digitalsys.api.views import index

router = routers.DefaultRouter()
router.register(r"credit_proposal", CreditProposalViewSet, basename="credit_proposal")

urlpatterns = [
    path(r"", index, name="index"),
    path(r"api/", include(router.urls)),
]
