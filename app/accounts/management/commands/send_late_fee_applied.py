from django.core.management.base import BaseCommand
from app.script_utils import send_balance_past_due_notification


class Command(BaseCommand):
    help = 'Send sms message for almost due loans'

    def handle(self, *args, **options):
        send_balance_past_due_notification()
