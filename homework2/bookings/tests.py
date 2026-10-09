"""Unit and integration tests for the bookings app."""
import datetime
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Booking, Movie, Seat
from .services import SeatUnavailable, book_seat, cancel_booking

User = get_user_model()


def make_movie(title="Test Movie"):
    return Movie.objects.create(
        title=title, description="desc", release_date=datetime.date(2024, 1, 1), duration=100)


# ------------------------------------------------------------------ models --

class ModelTests(TestCase):
    def test_str_representations(self):
        user = User.objects.create_user("bob", password="pw")
        movie, seat = make_movie(), Seat.objects.create(seat_number="A1")
        booking = Booking.objects.create(movie=movie, seat=seat, user=user)
        self.assertEqual(str(movie), "Test Movie")
        self.assertEqual(str(seat), "Seat A1")
        self.assertEqual(str(booking), "bob - Test Movie - Seat A1")

    def test_seat_defaults_to_available(self):
        self.assertFalse(Seat.objects.create(seat_number="A2").is_booked)

    def test_seat_number_must_be_unique(self):
        from django.db import IntegrityError, transaction
        Seat.objects.create(seat_number="A1")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Seat.objects.create(seat_number="A1")


# ---------------------------------------------------------------- services --

class ServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("amy", password="pw")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="B1")

    def test_book_seat_marks_seat_booked(self):
        booking = book_seat(self.user, self.movie, self.seat)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)
        self.assertEqual(booking.user, self.user)

    def test_double_booking_raises(self):
        book_seat(self.user, self.movie, self.seat)
        with self.assertRaises(SeatUnavailable):
            book_seat(self.user, self.movie, self.seat)
        self.assertEqual(Booking.objects.count(), 1)

    def test_cancel_frees_seat(self):
        booking = book_seat(self.user, self.movie, self.seat)
        cancel_booking(booking)
        self.seat.refresh_from_db()
        self.assertFalse(self.seat.is_booked)
        self.assertEqual(Booking.objects.count(), 0)


# --------------------------------------------------------------------- API --

class MovieApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@a.com", "pw")
        self.user = User.objects.create_user("user", password="pw")
        self.payload = {"title": "New", "description": "d", "release_date": "2024-02-02", "duration": 90}

    def test_list_is_public(self):
        make_movie()
        res = self.client.get("/api/movies/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(set(res.json()[0]), {"id", "title", "description", "release_date", "duration"})

    def test_retrieve(self):
        movie = make_movie()
        res = self.client.get(f"/api/movies/{movie.pk}/")
        self.assertEqual(res.json()["title"], "Test Movie")

    def test_anonymous_cannot_create(self):
        res = self.client.post("/api/movies/", self.payload)
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_regular_user_cannot_create(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post("/api/movies/", self.payload).status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_crud(self):
        self.client.force_authenticate(self.admin)
        res = self.client.post("/api/movies/", self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        pk = res.json()["id"]
        res = self.client.patch(f"/api/movies/{pk}/", {"title": "Renamed"})
        self.assertEqual(res.json()["title"], "Renamed")
        self.assertEqual(self.client.delete(f"/api/movies/{pk}/").status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)

    def test_invalid_movie_rejected(self):
        self.client.force_authenticate(self.admin)
        res = self.client.post("/api/movies/", {"title": "x"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class SeatApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", password="pw")
        self.movie = make_movie()
        self.free = Seat.objects.create(seat_number="A1")
        self.taken = Seat.objects.create(seat_number="A2", is_booked=True)

    def test_list_seats(self):
        self.assertEqual(len(self.client.get("/api/seats/").json()), 2)

    def test_filter_available(self):
        res = self.client.get("/api/seats/?available=true").json()
        self.assertEqual([s["seat_number"] for s in res], ["A1"])

    def test_filter_unavailable(self):
        res = self.client.get("/api/seats/?available=false").json()
        self.assertEqual([s["seat_number"] for s in res], ["A2"])

    def test_book_requires_login(self):
        res = self.client.post(f"/api/seats/{self.free.pk}/book/", {"movie": self.movie.pk})
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_book_seat(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(f"/api/seats/{self.free.pk}/book/", {"movie": self.movie.pk})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.free.refresh_from_db()
        self.assertTrue(self.free.is_booked)

    def test_book_taken_seat_fails(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(f"/api/seats/{self.taken.pk}/book/", {"movie": self.movie.pk})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_book_with_missing_movie_fails(self):
        self.client.force_authenticate(self.user)
        res = self.client.post(f"/api/seats/{self.free.pk}/book/", {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seats_are_read_only(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post("/api/seats/", {"seat_number": "Z9"}).status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class BookingApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", password="pw")
        self.other = User.objects.create_user("other", password="pw")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="A1")
        self.seat2 = Seat.objects.create(seat_number="A2")

    def test_requires_authentication(self):
        res = self.client.get("/api/bookings/")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_booking(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/bookings/", {"movie": self.movie.pk, "seat": self.seat.pk})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.json()["user"], "user")
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

    def test_cannot_double_book(self):
        book_seat(self.other, self.movie, self.seat)
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/bookings/", {"movie": self.movie.pk, "seat": self.seat.pk})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("seat", res.json())

    def test_history_only_shows_own_bookings(self):
        book_seat(self.user, self.movie, self.seat)
        book_seat(self.other, self.movie, self.seat2)
        self.client.force_authenticate(self.user)
        res = self.client.get("/api/bookings/").json()
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["seat"], self.seat.pk)

    def test_cannot_view_others_booking(self):
        booking = book_seat(self.other, self.movie, self.seat)
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.get(f"/api/bookings/{booking.pk}/").status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_booking_frees_seat(self):
        booking = book_seat(self.user, self.movie, self.seat)
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.delete(f"/api/bookings/{booking.pk}/").status_code,
                         status.HTTP_204_NO_CONTENT)
        self.seat.refresh_from_db()
        self.assertFalse(self.seat.is_booked)

    def test_invalid_ids_rejected(self):
        self.client.force_authenticate(self.user)
        res = self.client.post("/api/bookings/", {"movie": 999, "seat": 999})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------------------- HTML views --

class TemplateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", password="pw")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="A1")

    def test_movie_list_page(self):
        res = self.client.get(reverse("movie_list"))
        self.assertContains(res, "Test Movie")
        self.assertContains(res, "bootstrap")

    def test_movie_list_empty(self):
        Movie.objects.all().delete()
        self.assertContains(self.client.get(reverse("movie_list")), "No movies")

    def test_booking_requires_login(self):
        res = self.client.get(reverse("book_seat", args=[self.movie.pk]))
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login/", res.url)

    def test_seat_page_renders(self):
        self.client.login(username="user", password="pw")
        self.assertContains(self.client.get(reverse("book_seat", args=[self.movie.pk])), "A1")

    def test_seat_page_404_for_unknown_movie(self):
        self.client.login(username="user", password="pw")
        self.assertEqual(self.client.get(reverse("book_seat", args=[999])).status_code, 404)

    def test_book_via_form(self):
        self.client.login(username="user", password="pw")
        res = self.client.post(reverse("book_seat", args=[self.movie.pk]), {"seat": self.seat.pk})
        self.assertRedirects(res, reverse("booking_history"))
        self.assertEqual(Booking.objects.count(), 1)

    def test_book_taken_seat_via_form_shows_error(self):
        book_seat(self.user, self.movie, self.seat)
        self.client.login(username="user", password="pw")
        res = self.client.post(reverse("book_seat", args=[self.movie.pk]), {"seat": self.seat.pk}, follow=True)
        self.assertContains(res, "already booked")
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_history_page(self):
        book_seat(self.user, self.movie, self.seat)
        self.client.login(username="user", password="pw")
        self.assertContains(self.client.get(reverse("booking_history")), "Test Movie")

    def test_booking_history_empty(self):
        self.client.login(username="user", password="pw")
        self.assertContains(self.client.get(reverse("booking_history")), "no bookings")

    def test_cancel_booking_via_form(self):
        booking = book_seat(self.user, self.movie, self.seat)
        self.client.login(username="user", password="pw")
        self.client.post(reverse("cancel_booking", args=[booking.pk]))
        self.assertEqual(Booking.objects.count(), 0)

    def test_cannot_cancel_someone_elses_booking(self):
        other = User.objects.create_user("other", password="pw")
        booking = book_seat(other, self.movie, self.seat)
        self.client.login(username="user", password="pw")
        self.assertEqual(self.client.post(reverse("cancel_booking", args=[booking.pk])).status_code, 404)
        self.assertEqual(Booking.objects.count(), 1)

    def test_cancel_requires_post(self):
        booking = book_seat(self.user, self.movie, self.seat)
        self.client.login(username="user", password="pw")
        self.assertEqual(self.client.get(reverse("cancel_booking", args=[booking.pk])).status_code, 405)

    def test_signup_creates_user_and_logs_in(self):
        res = self.client.post(reverse("signup"), {
            "username": "newbie", "password1": "S3cure-pass-99", "password2": "S3cure-pass-99"})
        self.assertRedirects(res, reverse("movie_list"))
        self.assertTrue(User.objects.filter(username="newbie").exists())

    def test_signup_page_and_login_page_render(self):
        self.assertEqual(self.client.get(reverse("signup")).status_code, 200)
        self.assertEqual(self.client.get(reverse("login")).status_code, 200)

    def test_invalid_signup_rerenders(self):
        res = self.client.post(reverse("signup"), {"username": "x", "password1": "a", "password2": "b"})
        self.assertEqual(res.status_code, 200)


class SeedCommandTests(TestCase):
    def test_seed_is_idempotent(self):
        call_command("seed_data", stdout=StringIO())
        call_command("seed_data", stdout=StringIO())
        self.assertEqual(Movie.objects.count(), 3)
        self.assertEqual(Seat.objects.count(), 40)
