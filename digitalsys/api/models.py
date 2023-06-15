import uuid

from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from model_utils import Choices

CreditChoices = Choices(
    ("pending", "PENDING", "pending"),
    ("denied", "DENIED", "denied"),
    ("approved", "APPROVED", "approved"),
)

FieldTypes = Choices(
    ("text", "TEXT", "text"),
    ("number", "NUMBER", "number"),
)


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
        verbose_name_plural = "Old Credit Proposals"
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


class Proposal(BaseModel):
    status = models.CharField(
        max_length=20,
        default=CreditChoices.PENDING,
        choices=CreditChoices,
        blank=False,
        null=False,
        verbose_name="Status da Proposta",
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "Proposals"
        ordering = ["-created_at"]


class ProposalFields(BaseModel):
    field_name = models.CharField(
        max_length=60, blank=False, null=False, verbose_name="Nome do Campo"
    )
    field_title = models.CharField(
        max_length=60, blank=False, null=False, verbose_name="Título do Campo"
    )
    field_type = models.CharField(
        max_length=20,
        choices=FieldTypes,
        blank=False,
        null=False,
        verbose_name="Tipo do Campo",
    )

    def __str__(self):
        return f"{str(self.field_name)} - {self.field_title}"

    class Meta:
        verbose_name_plural = "Proposal Fields"
        ordering = ["created_at"]


class ProposalFieldsValue(BaseModel):
    field = models.ForeignKey(
        to=ProposalFields,
        related_name="proposal_field",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Campo",
    )
    proposal = models.ForeignKey(
        to=Proposal,
        related_name="proposal",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Nº da Proposta",
    )
    field_value = models.CharField(
        max_length=60, blank=False, null=False, verbose_name="Valor do Campo"
    )

    class Meta:
        verbose_name_plural = "Proposal Fields Values"
        ordering = ["created_at"]
