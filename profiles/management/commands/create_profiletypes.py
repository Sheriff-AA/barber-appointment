from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.conf import settings

from profiles.models import ProfileType

class Command(BaseCommand):

    PROFILE_PERMISSIONS = settings.PROFILE_PERMISSIONS

        
    def handle(self, *args, **kwargs):
        # Get the content type for the app's models (you can replace 'myapp' with your actual app)
        content_type = ContentType.objects.get_for_model(apps.get_model('profiles', 'ProfileType'))

        # Loop through the PROFILE_PERMISSIONS and create the permission objects
        for codename, name in self.PROFILE_PERMISSIONS:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Permission '{name}' created."))
            else:
                self.stdout.write(f"Permission '{name}' already exists.")

            # Create or get the group with the same name as the permission codename
            group, group_created = Group.objects.get_or_create(name=f"{codename.capitalize()} User Group")

            if group_created:
                self.stdout.write(self.style.SUCCESS(f"Group '{group.name}' created."))
            else:
                self.stdout.write(f"Group '{group.name}' already exists.")

            # Assign the permission to the group
            group.permissions.add(permission)
            self.stdout.write(self.style.SUCCESS(f"Permission '{name}' added to group '{group.name}'."))

             # Create or get the ProfileType
            profile_type, profile_created = ProfileType.objects.get_or_create(
                name=f"{codename.capitalize()} Proile Type",
                permissions=permission  # Assign the permission to ProfileType
            )

            # Add the group to the profile_type
            profile_type.groups.add(group)
            
            if profile_created:
                self.stdout.write(self.style.SUCCESS(f"ProfileType '{profile_type.name}' created and associated with group '{group.name}' and permission '{name}'."))
            else:
                self.stdout.write(f"ProfileType '{profile_type.name}' already exists and updated with group '{group.name}'.")

        self.stdout.write(self.style.SUCCESS("All permissions and groups have been processed."))