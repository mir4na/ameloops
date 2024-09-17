from django.core.management.base import BaseCommand
from main.models import Product

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('product_id', type=str, help='product id')

    def handle(self, *args, **kwargs):
        product_id = kwargs['product_id']
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            self.stdout.write(self.style.SUCCESS(f'{product} deleted'))
        except Product.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'not exist'))
