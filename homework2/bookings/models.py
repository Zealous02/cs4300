"""Data models for the movie theater booking app."""
from django.conf import settings
from django.db import models


class Movie(models.Model):
    """A movie that can be shown at the theater."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Seat(models.Model):
    """A physical seat in the theater and whether it is currently booked."""

    seat_number = models.CharField(max_length=10, unique=True)
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ["seat_number"]

    def __str__(self):
        return f"Seat {self.seat_number}"


class Booking(models.Model):
    """A user's reservation of one seat for one movie."""

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="bookings")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-booking_date"]

    def __str__(self):
        return f"{self.user} - {self.movie} - {self.seat}"
