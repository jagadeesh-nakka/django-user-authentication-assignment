# Django User Authentication Assignment

This project is a Django-based application that implements user authentication features, such as login, signup, password reset, and profile management. It includes the following pages:

- Login
- Signup
- Forgot Password
- Change Password
- Dashboard
- Profile

## Features

- **Login Page**: Users can log in using their email/username and password.
- **Signup Page**: New users can sign up with a username, email, password, and confirm password.
- **Forgot Password**: Users can reset their password via email.
- **Change Password**: Authenticated users can change their password.
- **Dashboard**: Displays a greeting to authenticated users and provides links to the Profile and Change Password pages.
- **Profile Page**: Displays the user's profile with information like username, email, and account details.

## Technologies Used

- **Django**: Web framework for Python.
- **HTML/CSS**: For structuring and styling the pages.
- **Email Backend**: Django's built-in email system to send password reset links.

## Requirements

- Python 3.8+
- Django 3.x+
- MySQL 5.x+
- An SMTP email service (for sending password reset emails, configure email settings in Django).

## Database Configuration

This project uses **MySQL** as the database. To set up the database, follow these steps:

1. **Install MySQL** on your machine if it's not already installed. You can download it from [MySQL's official website](https://dev.mysql.com/downloads/installer/).
2. **Install MySQL Client** for Django:
    ```bash
    pip install mysqlclient
    ```
    If you face issues, you can use `pymysql` as an alternative:
    ```bash
    pip install pymysql
    ```
    And add the following to the top of your `settings.py` file:
    ```python
    import pymysql
    pymysql.install_as_MySQLdb()
    ```

3. **Update `settings.py`**: In your Django project, go to the `settings.py` file and configure the database settings:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'web',  # Your database name
            'USER': 'root',  # Your MySQL username
            'PASSWORD': 'root',  # Your MySQL password
            'HOST': 'localhost',  # If you're using a local MySQL server
            'PORT': '3306',  # Default MySQL port
        }
    }
    ```

4. **Create the MySQL Database**: Before running migrations, ensure the database exists. You can create it from the MySQL shell:
    ```sql
    CREATE DATABASE web;
    ```

5. **Run Migrations**: Apply the migrations to create necessary tables in the database:
    ```bash
    python manage.py migrate
    ```

6. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

The project will be accessible at `http://127.0.0.1:8000/` in your browser.

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/your-username/django-user-authentication-assignment.git
