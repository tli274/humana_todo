# Django To-Do API
This is a simple Django REST API for managing to-do items. The API supports user registration, login with token-based authentication, and CRUD operations on to-do lists.

# Features
- User Registration & Login (Token-based Auth)
- CRUD operations for To-Do items
- Protected API routes
- Pytest test suite with Django integration
- Debug toolbar for performance profiling

# Tech Stack
- Django
- Django REST Framework
- Pytest / pytest-django
- DRF Simple JWT 
- SQLite 
- Django Debug Toolbar

# Installation (Make sure venv is activated)
- python -m venv venv
- (activate venv)
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py create_groups
- python manage.py runserver

# Run Test
pytest