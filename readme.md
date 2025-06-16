# Django Job Board Backend

A scalable and modular backend system for a job board application built with Django and Django REST Framework. This backend provides APIs for job listings, user authentication, applications, employer dashboards, and more.

## Features

- ✅ User Registration & Authentication (JWT)
- 🧑‍💼 Employer and Job Seeker Roles
- 📄 Job Posting, Editing, and Deletion (Employer)
- 🔍 Job Browsing and Filtering (Job Seeker)
- 📩 Job Applications Management
- 📊 Employer Dashboard API
- 🌐 Fully RESTful API (DRF)
- 🛡️ Permissions & Role-based Access Control
- 🔗 CORS & API token security setup
- 📁 Modular project structure

## Tech Stack

- Python 3.10+
- Django 4.x
- Django REST Framework
- PostgreSQL (or SQLite for local dev)
- JWT Authentication (via `djangorestframework-simplejwt`)
- CORS headers (`django-cors-headers`)

## Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.10+
- pip
- virtualenv (optional but recommended)
- PostgreSQL (or use SQLite for testing)

### Clone the Repository

```bash
git clone https://github.com/erajeetkumar/jobboard-backend
cd job-board-backend
```plaintext

### Setup Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a .env file in the root directory and set the following:

```plaintext

DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_DB=job_board
POSTGRES_USER=job_board
POSTGRES_PASSWORD=1313123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### If using SQLite for testing:

```plaintext
DATABASE_URL=sqlite:///db.sqlite3

```

## Run Migrations

```bash
python manage.py migrate
```

## Create Superuser and Start the server

```bash
python manage.py createsuperuser
python manage.py runserver

```

### API Endpoints

coming soon

## 🙌 Contribute or Star

If this project helped you, please ⭐ it or share with other devs. Contributions are welcome via pull requests!

[![Built by WebAcer Software](https://img.shields.io/badge/built%20by-WebAcer%20Software-blue)](https://webacersoftware.com/)

## 🔗 See Also

Want to see how we handled real-world Zoom API integration with HubSpot?

👉 Check out our [HubSpot + Zoom Webinar WordPress Plugin Case Study](https://webacersoftware.com/work/hubspot-with-zoom-webinar-integration/)

Explore more developer tools and integrations by [WebAcer Software](https://webacersoftware.com/).



