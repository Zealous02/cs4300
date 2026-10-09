"""Serializers that convert models to/from JSON."""
from rest_framework import serializers

from .models import Booking, Movie, Seat
from .services import SeatUnavailable, book_seat


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "seat_number", "is_booked"]
        read_only_fields = ["is_booked"]


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "movie", "seat", "user", "booking_date"]
        read_only_fields = ["booking_date"]

    def create(self, validated_data):
        """Create via the service so the seat is locked and marked booked."""
        try:
            return book_seat(validated_data["user"], validated_data["movie"], validated_data["seat"])
        except SeatUnavailable as exc:
            raise serializers.ValidationError({"seat": str(exc)})
