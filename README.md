# SpeedLogger

SpeedLogger is a full-stack Django web application for documenting, searching, and reporting internet speed test results across customers and sites.

## Project Purpose

SpeedLogger is designed for managed service providers, network technicians, and IT administrators who need a centralized system for storing historical internet performance test results. The application allows authenticated users to manage customers, sites, and speed test records through a browser-based interface.

## Technology Stack

SpeedLogger uses Python, Django, PostgreSQL-compatible database configuration, Bootstrap, Docker, GitLab, and Gunicorn.

## Core Features

SpeedLogger includes authenticated user access, customer management, site management, speed test record management, search functionality, timestamped report generation, form validation, and a responsive web interface.

## Local Development Setup

Clone the repository.

```bash
git clone <repository-url>
cd d424-software-engineering-capstone
```

Create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Apply database migrations.

```bash
python manage.py migrate
```

Create a local superuser.

```bash
python manage.py createsuperuser
```

Run the development server.

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## Docker Setup

Build and run the Docker container.

```bash
docker compose build
docker compose up
```

The Docker configuration runs database migrations, collects static files, and starts the application with Gunicorn.

Open the application at:

```text
http://127.0.0.1:8000/
```

Stop the container.

```bash
docker compose down
```

## Environment Variables

The application supports environment-based configuration. Use `.env.example` as a reference for required variables.

Important variables include:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS
DJANGO_CSRF_TRUSTED_ORIGINS
DATABASE_URL
DJANGO_SUPERUSER_USERNAME
DJANGO_SUPERUSER_EMAIL
DJANGO_SUPERUSER_PASSWORD
```

Do not commit real `.env` files or production secrets.

## Running Tests

Run the Django test suite with:

```bash
python manage.py test
```

## Maintenance Notes

A future developer should update dependencies through `requirements.txt`, apply migrations after model changes, run tests before deployment, and verify the application locally before pushing changes to GitLab.

When database models are changed, create and apply migrations.

```bash
python manage.py makemigrations
python manage.py migrate
```

Before deployment, run:

```bash
python manage.py check
python manage.py test
```

## Demo Login

For the demonstration environment, evaluator credentials may be created using the Docker environment variables in `docker-compose.yml`.

These credentials are intended only for capstone evaluation and should be changed or removed in a production environment.
