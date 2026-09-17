# AHF Uganda - Patient Management System

Phase 2 Industrial Training deliverable: a web-based Patient Management System
built with Django 5, MySQL 8, and Bootstrap 5, for the MySQL database designed
in Phase 1.

## Features

- **Authentication** - login/logout, role-based access (Admin, Doctor, Nurse,
  Receptionist, Lab Technician).
- **Patient Management** - register, search, view, update, soft-delete/restore.
- **Appointment Management** - schedule, update, cancel, view upcoming.
- **Visit Management** - record visits with vitals, view visit history.
- **Laboratory Management** - request tests, capture results, view lab history.
- **Dashboard** - total patients, today's appointments, missed appointments,
  recent visits.
- **Reports** - patient register, appointment report, visit report, laboratory
  report, each filterable by date range and exportable to CSV.

## Tech Stack

| Layer      | Choice                                   |
|------------|-------------------------------------------|
| Language   | Python 3.13+                              |
| Framework  | Django 5.x                                |
| Database   | MySQL 8.0 (via PyMySQL driver)            |
| Frontend   | Django Templates, Bootstrap 5, HTML/CSS/JS|
| ORM        | Django ORM                                |
| Forms      | django-crispy-forms + crispy-bootstrap5   |

## Project Structure

```
hosi/
├── config/          # Project settings, root URLs, WSGI/ASGI
├── accounts/        # Custom user model, roles, login/logout, staff admin
├── patients/         # Patient registration, search, soft delete
├── appointments/     # Appointment scheduling
├── visits/           # Patient visit records & vitals
├── laboratory/       # Lab test requests & results
├── dashboard/        # Dashboard/home view
├── reports/          # Reports (patient/appointment/visit/lab + CSV export)
├── templates/         # Base template + shared partials
├── static/            # Custom CSS/JS
└── media/              # Uploaded files (if any)
```

## Getting Started

See [INSTALLATION.md](INSTALLATION.md) for the full setup guide (Python,
MySQL, virtual environment, environment variables, migrations, and running
the dev server).

Quick start once prerequisites are installed:

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # then edit DB credentials
mysql -u root -p -e "CREATE DATABASE ahf_pms CHARACTER SET utf8mb4;"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit http://127.0.0.1:8000/accounts/login/

## Roles

| Role          | Typical Access                                   |
|---------------|---------------------------------------------------|
| Administrator | Full access, manages staff accounts               |
| Doctor        | Patients, appointments, visits, lab tests          |
| Nurse         | Patients, visits, lab tests                        |
| Receptionist  | Patient registration, appointment scheduling       |
| Lab Technician| Lab test requests & results                        |

Role checks are enforced with `accounts.decorators.role_required` /
`RoleRequiredMixin`; superusers always have full access. Assign roles from
Django admin (`/admin/`) or the in-app Staff Accounts screen (admin only).

## Database

The application reuses the entity design from the Phase 1 MySQL database
(patients, appointments, visits, laboratory tests/results, staff/users),
expressed here as Django models under each app's `models.py`. Run
`python manage.py makemigrations` and `python manage.py migrate` to create
the schema in MySQL - see INSTALLATION.md for details.
