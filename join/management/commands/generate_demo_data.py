from django.core.management.base import BaseCommand
from join.management.commands.init_demo_data import generate_demo_data

class Command(BaseCommand):
    help = 'Generate demo data for tasks, contacts, and subtasks'

    def handle(self, *args, **kwargs):
        generate_demo_data(sender=self.__class__, user=None)
        self.stdout.write(self.style.SUCCESS('Demo data generation completed successfully.'))
