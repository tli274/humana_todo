from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create default user and admin groups if they do not exist'

    def handle(self, *args, **kwargs):
        # Create 'user' group if it doesn't exist
        user_group, created = Group.objects.get_or_create(name='user')
        if created:
            self.stdout.write(self.style.SUCCESS("Created 'user' group"))

        # Create 'admin' group if it doesn't exist
        admin_group, created = Group.objects.get_or_create(name='admin')
        if created:
            self.stdout.write(self.style.SUCCESS("Created 'admin' group"))
        else:
            self.stdout.write(self.style.SUCCESS("'admin' group already exists"))