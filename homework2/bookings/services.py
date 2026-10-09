"""Shared booking logic used by both the REST API and the HTML views."""
from django.db import transaction

from .models import Booking, Seat


class SeatUnavailable(Exception):
    """Raised when the requested seat is already booked."""


def book_seat(user, movie, seat):
    """Atomically book `seat` for `user` to see `movie`.

    Raises SeatUnavailable if the seat has already been taken.
    """
    with transaction.atomic():
        locked = Seat.objects.select_for_update().get(pk=seat.pk)
        if locked.is_booked:
            raise SeatUnavailable(f"{locked} is already booked.")
        locked.is_booked = True
        locked.save(update_fields=["is_booked"])
        return Booking.objects.create(user=user, movie=movie, seat=locked)


def cancel_booking(booking):
    """Delete a booking and free its seat."""
    with transaction.atomic():
        seat = Seat.objects.select_for_update().get(pk=booking.seat_id)
        booking.delete()
        seat.is_booked = False
        seat.save(update_fields=["is_booked"])
