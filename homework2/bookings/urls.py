"""URL routes: HTML pages plus the REST API."""
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("movies", views.MovieViewSet, basename="movie")
router.register("seats", views.SeatViewSet, basename="seat")
router.register("bookings", views.BookingViewSet, basename="booking")

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/book/", views.seat_booking, name="book_seat"),
    path("history/", views.booking_history, name="booking_history"),
    path("history/<int:booking_id>/cancel/", views.cancel_booking_view, name="cancel_booking"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/", include(router.urls)),
]
