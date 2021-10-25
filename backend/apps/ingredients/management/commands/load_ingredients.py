import csv

from django.core.management.base import BaseCommand
from ingredients.models import Ingredient


class Command(BaseCommand):
    help = 'Загругзка тестовых данных'

    def handle(self, *args, **options):
        if self._is_empty_data_base():
            self._record_data_in_db('../data/ingredients.csv')

    def _is_empty_data_base(self):
        if Ingredient.objects.all().count() != 0:
            return False
        return True

    def _record_data_in_db(self, file_path):
        with open(file_path,
                  newline='',) as csvfile:

            reader = csv.reader(csvfile)
            for row in reader:
                name, measurement_unit = row

                Ingredient.objects.create(
                    name=name,
                    measurement_unit=measurement_unit
                )

    def _clear_data_base(self):
        Ingredient.objects.all().delete()
