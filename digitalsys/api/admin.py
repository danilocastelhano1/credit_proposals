from django.contrib import admin

# Register your models here.
from digitalsys.api.models import CreditProposal


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
