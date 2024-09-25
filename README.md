# Django Task Management Backend

This repository contains the backend code for a task management system developed using Django and Django REST Framework (DRF). It supports user authentication, task and subtask management, contact management, and assignment of contacts to tasks.

## Features

- **User Authentication**: Token-based authentication system using Django's built-in user model and DRF's token authentication.
- **Task Management**: Create, update, retrieve, and delete tasks with support for categories, priorities, status, due dates, and subtasks.
- **Subtask Management**: Each task can have multiple subtasks, which can be managed independently.
- **Contact Management**: Manage contacts, with the ability to assign contacts to tasks.
- **Sphinx Documentation**: Docstrings have been added across views, models, serializers, and admin modules to generate automated documentation using Sphinx.

## Project Structure

- **models.py**: Contains the database models for tasks, subtasks, and contacts, as well as many-to-many relationships between tasks and contacts.
- **views.py**: API views for handling task, subtask, and contact-related requests.
- **serializers.py**: DRF serializers for converting complex data types like model instances into native Python datatypes.
- **admin.py**: Custom admin interface to manage tasks, subtasks, and contacts.
- **urls.py**: Contains all URL routing for API endpoints.
- **Sphinx Documentation**: Docstrings have been added to the key files (`views.py`, `models.py`, `serializers.py`, and `admin.py`) for generating documentation.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BenjaminTietz/join-backend.git
   cd join-backend
2. Set up the virtual environment and install dependencies:
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
3. Run database migrations:
   python manage.py migrate
4. Create a superuser:
   python manage.py createsuperuser
5. Start the development server:
   python manage.py runserver

API Endpoints

Authentication
- Login: /login/ (POST)
- Signup: /signup/ (POST)

Tasks
- List all tasks: /tasks/ (GET)
- Create a task: /tasks/ (POST)
- Retrieve a task: /tasks/{task_id}/ (GET)
- Update a task: /tasks/{task_id}/ (PATCH)
- Add subtasks: /tasks/{task_id}/subtasks/ (POST)
- Assign contacts: /tasks/{task_id}/assignees/ (POST)

Contacts
- List all contacts: /contacts/ (GET)
- Create a contact: /contacts/ (POST)
- Retrieve a contact: /contacts/{contact_id}/ (GET)
- Update a contact: /contacts/{contact_id}/ (PATCH)

Testing
To run tests, use the following command:
python manage.py test

Documentation
This project is documented using Sphinx. To generate the documentation locally:

1. Install Sphinx:
pip install sphinx

2. Generate the documentation:
   cd docs
   make html
4. Open the documentation:
   open _build/html/index.html

Contributing
Feel free to open issues or submit pull requests if you'd like to contribute to the project.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
