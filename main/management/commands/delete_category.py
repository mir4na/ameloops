from django.core.management.base import BaseCommand
from main.models import Category

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('category_id', type=str, help='category id')

    def handle(self, *args, **kwargs):
        category_id = kwargs['category_id']
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            self.stdout.write(self.style.SUCCESS(f'{category} deleted'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'not exist'))