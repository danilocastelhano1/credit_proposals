from typing import List

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from digitalsys.api.models import CreditProposal
from digitalsys.api.models import FieldTypes
from digitalsys.api.models import ProposalFields
from digitalsys.api.utils import generate_cpf


class Command(BaseCommand):
    help = "Seed the database informations"

    def create_regular_user(self):
        if User.objects.filter(username="jon").count() == 0:
            self.stdout.write(
                self.style.WARNING(
                    "Iniciando o processo de Inserção de um usuário normal"
                )
            )
            user = User.objects.create_user(
                username="jon", email="jon@doe.com", password="123456", is_staff=True
            )
            self.stdout.write(
                self.style.SUCCESS("processo de criação de Usuário Finalizado")
            )

            user.user_permissions.add(
                Permission.objects.get(codename="view_creditproposal"),
                Permission.objects.get(codename="view_proposal"),
                Permission.objects.get(codename="view_proposalfields"),
                Permission.objects.get(codename="view_proposalfieldsvalue"),
            )

    def create_super_user(self):
        if User.objects.filter(username="admin").count() == 0:
            self.stdout.write(
                self.style.WARNING("Iniciando o processo de Inserção de Super User")
            )
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write(
                self.style.SUCCESS("processo de criação de Super User Finalizado")
            )

    def create_credit_proposals(self):
        if CreditProposal.objects.count() > 0:
            return

        for i in range(1, 10):
            CreditProposal.objects.create(
                fullname=f"Proposal {str(i)}",
                cpf=generate_cpf(),
                address=f"Address {str(i)}",
                proposal_value=i * 12,
            )

    def create_proposals_field(self):
        if ProposalFields.objects.count() > 0:
            return
        proposal_fields_list: List[ProposalFields] = [
            ProposalFields(
                field_name="full_name",
                field_title="Nome Completo",
                field_type=FieldTypes.TEXT,
            ),
            ProposalFields(
                field_name="cpf",
                field_title="CPF do Cliente",
                field_type=FieldTypes.TEXT,
            ),
            ProposalFields(
                field_name="address",
                field_title="Endereço do Cliente",
                field_type=FieldTypes.TEXT,
            ),
            ProposalFields(
                field_name="proposal_value",
                field_title="Valor da Proposta",
                field_type=FieldTypes.NUMBER,
            ),
        ]

        ProposalFields.objects.bulk_create(proposal_fields_list)

    def handle(self, *args, **options):
        self.create_regular_user()
        self.create_super_user()

        self.create_proposals_field()
