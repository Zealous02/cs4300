Feature: Booking movie seats
  As a movie fan
  I want to browse movies, book a seat and see my bookings
  So that I can plan my night out

  Background:
    Given a movie "Dune" exists
    And seats "A1" and "A2" exist
    And I am a logged in user "fan"

  Scenario: Viewing the movie listings
    When I visit the movie list page
    Then I should see "Dune"

  Scenario: Booking an available seat
    When I book seat "A1" for "Dune"
    Then I should be on my booking history page
    And I should see "A1"
    And seat "A1" should be marked as booked

  Scenario: Booking a seat that is already taken
    Given seat "A1" has already been booked by someone else
    When I book seat "A1" for "Dune"
    Then I should see "already booked"

  Scenario: Booking history through the API
    Given I have booked seat "A2" for "Dune"
    When I request my bookings from the API
    Then the API response should contain 1 booking
