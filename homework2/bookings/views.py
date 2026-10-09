"""REST API viewsets and template-based views."""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Booking, Movie, Seat
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer
from .services import SeatUnavailable, book_seat, cancel_booking


# ---------------------------------------------------------------- REST API --

class MovieViewSet(viewsets.ModelViewSet):
    """CRUD for movies. Anyone can read; only staff can modify."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    """Seat availability (``?available=true`` filters) and booking."""

    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        available = self.request.query_params.get("available")
        if available is not None:
            qs = qs.filter(is_booked=available.lower() not in ("true", "1", "yes"))
        return qs

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def book(self, request, pk=None):
        """POST /api/seats/<id>/book/ with {"movie": <id>} books the seat."""
        seat = self.get_object()
        serializer = BookingSerializer(data={"movie": request.data.get("movie"), "seat": seat.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """A user's booking history, creating bookings, and cancelling them."""

    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related("movie", "seat")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        cancel_booking(instance)


# --------------------------------------------------------------- Templates --

def movie_list(request):
    """Landing page listing every movie."""
    return render(request, "bookings/movie_list.html", {"movies": Movie.objects.all()})


@login_required
def seat_booking(request, movie_id):
    """Show the seat map for a movie and book the chosen seat on POST."""
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        seat = get_object_or_404(Seat, pk=request.POST.get("seat") or 0)
        try:
            book_seat(request.user, movie, seat)
        except SeatUnavailable as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, f"Booked {seat} for {movie.title}!")
            return redirect("booking_history")
        return redirect("book_seat", movie_id=movie.pk)
    return render(request, "bookings/seat_booking.html", {"movie": movie, "seats": Seat.objects.all()})


@login_required
def booking_history(request):
    """List the logged-in user's bookings."""
    bookings = Booking.objects.filter(user=request.user).select_related("movie", "seat")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})


@login_required
@require_POST
def cancel_booking_view(request, booking_id):
    """Cancel one of the user's own bookings."""
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    cancel_booking(booking)
    messages.success(request, "Booking cancelled.")
    return redirect("booking_history")


def signup(request):
    """Register a new account and log in."""
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        return redirect("movie_list")
    return render(request, "registration/signup.html", {"form": form})
