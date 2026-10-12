from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update Admin superuser"

    def handle(self, *args, **kwargs):

        username = "csc"
        password = "csc"
        email = "annanagarcsc2024@gmail.com"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS("Admin superuser created successfully!")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Admin superuser updated successfully!")
            )

        self.stdout.write(f"Username : {username}")
        self.stdout.write(f"Password : {password}")
        self.stdout.write("Superuser: True")
        self.stdout.write("Staff    : True")