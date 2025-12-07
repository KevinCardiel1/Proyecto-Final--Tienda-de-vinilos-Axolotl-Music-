from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app_Axolotl.models import Usuario


class Command(BaseCommand):
    help = 'List all auth users and Usuario profiles (shows mapping)'

    def handle(self, *args, **options):
        User = get_user_model()
        self.stdout.write('--- Auth Users ---')
        for u in User.objects.all().order_by('username'):
            self.stdout.write(f"{u.pk}: username='{u.username}' email='{u.email}' is_staff={u.is_staff} is_superuser={u.is_superuser}")

        self.stdout.write('\n--- Usuario profiles ---')
        for p in Usuario.objects.all().order_by('id'):
            user_repr = p.user.username if p.user else None
            self.stdout.write(f"{p.pk}: nombre='{p.nombre}' email='{p.email}' linked_user='{user_repr}'")
