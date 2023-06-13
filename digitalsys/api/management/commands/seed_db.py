from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed the database informations"

    def create_regular_user(self):
        if User.objects.filter(username="jon").count() == 0:
            self.stdout.write(
                self.style.WARNING("Iniciando o processo de Inserção de um usuário normal")
            )
            user = User.objects.create_user(
                username="jon", email="jon@doe.com", password="123456", is_staff=True
            )
            self.stdout.write(
                self.style.SUCCESS("processo de criação de Usuário Finalizado")
            )

            user.user_permissions.add(Permission.objects.get(codename='view_creditproposal'))

    def create_super_user(self):
        if User.objects.filter(username="admin").count() == 0:
            self.stdout.write(
                self.style.WARNING("Iniciando o processo de Inserção de Super User")
            )
            User.objects.create_superuser(
                "admin", "admin@example.com", "admin"
            )
            self.stdout.write(
                self.style.SUCCESS("processo de criação de Super User Finalizado")
            )

    def handle(self, *args, **options):
        self.create_regular_user()
        self.create_super_user()
