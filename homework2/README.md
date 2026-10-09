# Homework 2 – Movie Theater Booking (Django + DRF)

A RESTful movie theater booking app. Users can browse movies, book seats, and see their booking
history, both through a Bootstrap web UI and through a JSON API.

**Render URL:** https://movie-theater-booking-wvzd.onrender.com

**GitHub:** https://github.com/Zealous02/cs4300/tree/main/homework2

## Project structure

```
homework2/
├── manage.py
├── movie_theater_booking/      # Django project (settings, root urls, wsgi)
├── bookings/                   # The app
│   ├── models.py               # Movie, Seat, Booking
│   ├── services.py             # book_seat / cancel_booking (atomic, shared by API + UI)
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # MovieViewSet, SeatViewSet, BookingViewSet + template views
│   ├── urls.py                 # HTML routes + /api/ router
│   ├── tests.py                # unit + integration tests
│   ├── management/commands/seed_data.py
│   └── templates/              # base, movie_list, seat_booking, booking_history, login, signup
├── features/                   # Behave (BDD) feature + steps
├── requirements.txt  build.sh  render.yaml
```

## Setup

```bash
python3 -m venv myenv --system-site-packages
source myenv/bin/activate          # Windows: myenv\Scripts\activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py seed_data        # 3 sample movies + 40 seats
python3 manage.py createsuperuser  # optional: needed to add/edit movies via the API/admin
python3 manage.py runserver 0.0.0.0:3000
```

In DevEdu, open the "app" button next to the editor (`https://app-<container>-<section>.devedu.io/`).

## Web UI

| Page | URL |
|---|---|
| Movie listings | `/` |
| Seat booking | `/movies/<id>/book/` (login required) |
| Booking history / cancel | `/history/` (login required) |
| Sign up / log in | `/signup/`, `/login/` |

## REST API

| Endpoint | Methods | Notes |
|---|---|---|
| `/api/movies/` , `/api/movies/<id>/` | GET (public); POST/PUT/PATCH/DELETE (staff only) | Full CRUD |
| `/api/seats/` | GET | `?available=true` / `?available=false` filters by availability |
| `/api/seats/<id>/book/` | POST `{"movie": <id>}` | Books the seat for the logged-in user |
| `/api/bookings/` | GET, POST `{"movie": <id>, "seat": <id>}` | Only the current user's bookings; double-booking returns 400 |
| `/api/bookings/<id>/` | GET, DELETE | DELETE cancels and frees the seat |

Authentication is by session (browsable API login) or HTTP Basic.

## Testing

```bash
python3 manage.py test                                   # 43 unit + integration tests
python3 manage.py behave                                 # BDD scenarios (Behave)
coverage run --source=bookings manage.py test && coverage report --omit="*/migrations/*,*/tests.py"
```

Coverage of the `bookings` app is 100%.

The app was run and tested locally in an Anaconda Prompt virtual environment (all tests pass, UI and API work) and is live on Render.

## Deployment (Render)

1. Push this repo to GitHub.
2. In Render choose **New → Blueprint** and select the repo; it reads `render.yaml`
   (root dir `homework2`, runs `build.sh`, starts `gunicorn`, attaches a free Postgres DB).
   Alternatively create a Web Service manually with root directory `homework2`,
   build command `./build.sh`, start command `gunicorn movie_theater_booking.wsgi:application`,
   and env vars `DEBUG=False`, `SECRET_KEY=<random>`, `DATABASE_URL=<postgres url>`.
3. Paste the resulting URL at the top of this README.

## AI usage citation

Claude (Anthropic's Claude Code, Sonnet 5.5) was used to generate the project scaffolding, models,
serializers, viewsets, templates, tests, Behave scenarios, deployment files and this README.
The generated code was reviewed, run (all tests pass), and incorporated into the project by Dominick.
