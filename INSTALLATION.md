# Installation Guide

## 1. Prerequisites

- **Python 3.13+** - https://www.python.org/downloads/ (on Windows, check
  "Add python.exe to PATH" during install; the Microsoft Store stub aliases
  do not count as a real install).
- **MySQL 8.0** - https://dev.mysql.com/downloads/installer/ (Community
  Server + MySQL Workbench are enough).
- **Git** - https://git-scm.com/downloads
- (Optional) **VS Code** with the Python extension.

Verify after installing:

```powershell
python --version
mysql --version
git --version
```

## 2. Get the project

```powershell
cd C:\Users\Admin\Desktop\hosi
git init                      # if not already a repository
git add .
git commit -m "Initial Django project scaffold"
```

## 3. Create a virtual environment

```powershell
python -m venv venv
venv\Scripts\Activate.ps1     # PowerShell
```

## 4. Install dependencies

```powershell
pip install -r requirements.txt
```

This installs Django, PyMySQL (pure-Python MySQL driver - no C build tools
needed on Windows), python-dotenv, and django-crispy-forms with the
Bootstrap 5 template pack.

## 5. Create the MySQL database

Open a MySQL shell (`mysql -u root -p`) or MySQL Workbench and run:

```sql
CREATE DATABASE ahf_pms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ahf_user'@'localhost' IDENTIFIED BY 'change-this-password';
GRANT ALL PRIVILEGES ON ahf_pms.* TO 'ahf_user'@'localhost';
FLUSH PRIVILEGES;
```

## 6. Configure environment variables

```powershell
copy .env.example .env
```

Edit `.env` and set:

```
DJANGO_SECRET_KEY=<a long random string>
DJANGO_DEBUG=True
DB_NAME=ahf_pms
DB_USER=ahf_user
DB_PASSWORD=change-this-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

## 7. Run migrations

```powershell
python manage.py makemigrations accounts patients appointments visits laboratory
python manage.py migrate
```

## 8. Create an administrator account

```powershell
python manage.py createsuperuser
```

Enter a username, email, and password. After first login, open
`/admin/` and set that user's **Role** to `Administrator` (the createsuperuser
flow does not prompt for the custom `role` field).

## 9. Run the development server

```powershell
python manage.py runserver
```

Visit http://127.0.0.1:8000/accounts/login/ and sign in.

## 10. Collect static files (production only)

```powershell
python manage.py collectstatic
```

## Troubleshooting

- **`django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")`**
  - Confirm MySQL is running (`services.msc` -> MySQL80) and `DB_HOST`/`DB_PORT`
    in `.env` are correct.
- **`Access denied for user`**
  - Re-check `DB_USER`/`DB_PASSWORD` and that the user was granted privileges
    on `ahf_pms` (step 5).
- **`ModuleNotFoundError: No module named 'django'`**
  - The virtual environment isn't activated - re-run
    `venv\Scripts\Activate.ps1`.
- **Login page loads but styles look broken**
  - Run `python manage.py collectstatic` in production, or in development
    make sure `DEBUG=True` so Django serves static files directly.
