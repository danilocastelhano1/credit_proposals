from django.contrib import admin

# Register your models here.
from digitalsys.api.models import CreditProposal
from digitalsys.api.models import Proposal
from digitalsys.api.models import ProposalFields
from digitalsys.api.models import ProposalFieldsValue


@admin.register(CreditProposal)
class CreditProposalAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    list_display = [
        "id",
        "fullname",
        "cpf",
        "address",
        "proposal_value",
        "status",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at", "status"]
    search_fields = ["id", "fullname", "cpf", "address"]


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    list_display = [
        "id",
        "status",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at", "status"]
    search_fields = ["id"]


@admin.register(ProposalFields)
class ProposalFieldsAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    list_display = [
        "id",
        "field_name",
        "field_title",
        "field_type",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at", "field_type"]
    search_fields = ["id", "field_name", "field_title", "field_type"]


@admin.register(ProposalFieldsValue)
class ProposalFieldsValueAdmin(admin.ModelAdmin):
    ordering = ["-created_at"]
    list_display = [
        "id",
        "get_proposal",
        "get_field_name",
        "get_field_title",
        "get_field_type",
        "field_value",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at"]
    search_fields = [
        "id",
        "proposal__id",
    ]

    @admin.display(ordering="proposal__id", description="Nº da Proposta")
    def get_proposal(self, obj: ProposalFieldsValue):
        return obj.proposal.id

    @admin.display(ordering="field__field_name", description="Nome do Campo")
    def get_field_name(self, obj: ProposalFieldsValue):
        return obj.field.field_name

    @admin.display(ordering="field__field_title", description="Título do Campo")
    def get_field_title(self, obj: ProposalFieldsValue):
        return obj.field.field_title

    @admin.display(ordering="field__field_type", description="Tipo do Campo")
    def get_field_type(self, obj: ProposalFieldsValue):
        return obj.field.field_type
