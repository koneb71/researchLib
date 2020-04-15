import os

from django.core.management.base import BaseCommand
from django.apps import apps
import pandas as pd

from app.models import PublicationType, Colleges, Departments


class Command(BaseCommand):
    help = "Pre-populate database"

    def handle(self, *args, **options):
        base_path = apps.get_app_config('app').path
        file_path = os.path.join(base_path, "management",
                                 "commands", "predata.csv")
        data = pd.read_csv(file_path).fillna('')
        df = data.to_dict(orient='records')

        for item in df:
            PublicationType.objects.create(name=item['publication_type'])
            if item['colleges']:
                college = Colleges.objects.create(name=item['colleges'])
                departments = str(item['departments']).split(', ')
                for dep in departments:
                    Departments.objects.create(name=dep, college=college)