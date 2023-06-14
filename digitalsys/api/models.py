import uuid

from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from model_utils import Choices


# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Id"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True
        indexes = [BrinIndex(fields=["created_at"])]


class CreditProposal(BaseModel):
    CreditChoices = Choices(
        ("pending", "PENDING", "pending"),
        ("denied", "DENIED", "denied"),
        ("approved", "APPROVED", "approved"),
    )

    fullname = models.CharField(max_length=80, blank=False, null=False)
    cpf = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    proposal_value = models.DecimalField(
        max_digits=12, decimal_places=2, blank=False, null=False
    )
    status = models.CharField(
        max_length=20,
        default=CreditChoices.PENDING,
        choices=CreditChoices,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name_plural = "Credit Proposals"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{str(self.cpf)} - {self.fullname}"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.cpf = "".join([i for i in self.cpf if i.isdigit()])

        return super(CreditProposal, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )
