from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Promote a user to staff and/or superuser. Usage: python manage.py promote_user <username> [--staff] [--super]'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to promote')
        parser.add_argument('--staff', action='store_true', help='Set is_staff=True')
        parser.add_argument('--super', dest='superuser', action='store_true', help='Set is_superuser=True')

    def handle(self, *args, **options):
        username = options.get('username')
        make_staff = options.get('staff')
        make_super = options.get('superuser')

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f"User with username '{username}' does not exist.")

        changed = False
        if make_staff and not user.is_staff:
            user.is_staff = True
            changed = True
        if make_super and not user.is_superuser:
            user.is_superuser = True
            changed = True

        if changed:
            user.save()
            self.stdout.write(self.style.SUCCESS(f"User '{username}' updated: is_staff={user.is_staff}, is_superuser={user.is_superuser}"))
        else:
            self.stdout.write(self.style.WARNING(f"No changes made for '{username}'. Current: is_staff={user.is_staff}, is_superuser={user.is_superuser}"))
