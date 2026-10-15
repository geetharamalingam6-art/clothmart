from django.core.management.base import BaseCommand

from shop.seed import seed_clothes_catalog


class Command(BaseCommand):
    help = "Create Men, Women, and Children clothing categories and sample products."

    def handle(self, *args, **options):
        seed_clothes_catalog()
        self.stdout.write(self.style.SUCCESS("Clothing catalog is ready."))
