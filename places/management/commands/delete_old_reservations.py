from django.core.management.base import BaseCommand
from places.models import Reservation
from datetime import date


class Command(BaseCommand):
    def handle(self, *args, **options):
        old_reservations = Reservation.objects.filter(date__lt=date.today())
        old_reservations.delete()
