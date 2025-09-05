Markety - Django E-commerce with Authentication

Quick start:
1) python -m venv venv
2) venv\Scripts\activate  (Windows)
3) pip install -r requirements.txt
4) python manage.py migrate
5) python manage.py createsuperuser
6) python manage.py runserver

Auth routes:
  /accounts/register/   -> sign up
  /accounts/login/      -> login
  /accounts/logout/     -> logout
  /accounts/profile/    -> profile + order history

Use the admin to add categories and products.
