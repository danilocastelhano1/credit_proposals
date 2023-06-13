import uuid

from django.contrib.postgres.indexes import BrinIndex
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True
        indexes = [BrinIndex(fields=["created_at"])]


class CreditProposal(BaseModel):
    fullname = models.CharField(max_length=80, blank=False, null=False)
    cpf = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    proposal_value = models.DecimalField(
        max_digits=12, decimal_places=2, blank=False, null=False
    )

    class Meta:
        verbose_name_plural = "Credit Proposals"

    def __str__(self):
        return f"{str(self.cpf)} - {self.fullname}"
