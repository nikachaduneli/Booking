from .models import Reservation
from datetime import date


def remove_old_reservations():
    old_reservations = Reservation.objects.filter(date__lt=date.today())
    old_reservations.delete()
