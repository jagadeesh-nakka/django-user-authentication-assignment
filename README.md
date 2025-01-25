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
- An SMTP email service (for sending password reset emails, configure email settings in Django).

## Installation

1. **Clone the repository:**
   ```bash
   git clone ""


2. **Navigate to the project directory:**
   ```bash
     -cd django-user-authentication-assignment


 3. **Install dependencies:**
   ```bash
   -pip install -r requirements.txt   


 4. **Run the development server:**
   
    -python manage.py runserver



