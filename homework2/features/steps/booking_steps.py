"""Behave step definitions (run via behave-django: `python manage.py behave`)."""
import datetime

from behave import given, then, when
from django.contrib.auth import get_user_model

from bookings.models import Booking, Movie, Seat
from bookings.services import book_seat

User = get_user_model()


@given('a movie "{title}" exists')
def step_movie(context, title):
    context.movie = Movie.objects.create(
        title=title, description="desc", release_date=datetime.date(2024, 1, 1), duration=120)


@given('seats "{a}" and "{b}" exist')
def step_seats(context, a, b):
    for number in (a, b):
        Seat.objects.create(seat_number=number)


@given('I am a logged in user "{username}"')
def step_login(context, username):
    context.user = User.objects.create_user(username, password="pw12345!")
    context.test.client.login(username=username, password="pw12345!")


@given('seat "{number}" has already been booked by someone else')
def step_taken(context, number):
    other = User.objects.create_user("someone", password="pw12345!")
    book_seat(other, context.movie, Seat.objects.get(seat_number=number))


@given('I have booked seat "{number}" for "{title}"')
def step_have_booked(context, number, title):
    book_seat(context.user, Movie.objects.get(title=title), Seat.objects.get(seat_number=number))


@when("I visit the movie list page")
def step_visit_list(context):
    context.response = context.test.client.get("/", follow=True)


@when('I book seat "{number}" for "{title}"')
def step_book(context, number, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(seat_number=number)
    context.response = context.test.client.post(f"/movies/{movie.pk}/book/", {"seat": seat.pk}, follow=True)


@when("I request my bookings from the API")
def step_api(context):
    context.response = context.test.client.get("/api/bookings/")


@then('I should see "{text}"')
def step_see(context, text):
    context.test.assertContains(context.response, text)


@then("I should be on my booking history page")
def step_on_history(context):
    context.test.assertEqual(context.response.request["PATH_INFO"], "/history/")


@then('seat "{number}" should be marked as booked')
def step_seat_booked(context, number):
    context.test.assertTrue(Seat.objects.get(seat_number=number).is_booked)


@then("the API response should contain {count:d} booking")
def step_api_count(context, count):
    context.test.assertEqual(context.response.status_code, 200)
    context.test.assertEqual(len(context.response.json()), count)
    context.test.assertEqual(Booking.objects.filter(user=context.user).count(), count)
