"""Populate the database with sample movies and a 5x8 seat grid."""
import datetime

from django.core.management.base import BaseCommand

from bookings.models import Movie, Seat

MOVIES = [
    ("The Last Frontier", "A pioneer family crosses a hostile continent.", datetime.date(2024, 5, 17), 128),
    ("Midnight Algorithm", "A hacker uncovers a conspiracy inside a trading firm.", datetime.date(2024, 8, 2), 112),
    ("Paper Moons", "An animated tale of two siblings and a lost lantern.", datetime.date(2025, 1, 24), 96),
]


class Command(BaseCommand):
    help = "Create sample movies and seats (idempotent)."

    def handle(self, *args, **options):
        for title, desc, date, minutes in MOVIES:
            Movie.objects.get_or_create(title=title, defaults={
                "description": desc, "release_date": date, "duration": minutes})
        for row in "ABCDE":
            for number in range(1, 9):
                Seat.objects.get_or_create(seat_number=f"{row}{number}")
        self.stdout.write(self.style.SUCCESS("Seeded movies and seats."))
