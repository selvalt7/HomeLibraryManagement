from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Load mock_data.json fixture into the database.'

    def handle(self, *args, **options):
        self.stdout.write('Loading mock_data.json fixture...')
        try:
            call_command('loaddata', 'mock_data.json')
            self.stdout.write(self.style.SUCCESS('Mock data loaded successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR('Failed to load mock data: %s' % str(e)))
