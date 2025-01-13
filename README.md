# Booking

This is a Django-based web application designed to handle bookings for various places. The app allows users to create and manage bookings and provides an admin interface to oversee user and booking management. Users can register, log in, and book places. Admins can manage users, places, and bookings.

## Features

- User authentication (registration, login, logout)
- Create and manage bookings
- Admin interface to manage users and bookings
- Manage places available for booking

## Installation

To install and run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/nikachaduneli/Booking.git
2. Navigate to the project directory
   ```bash
    cd Booking
3. Create a virtual environment (optional but recommended):
   ```bash
    python -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
5. Apply migrations
    ```bash
   python manage.py makemigrations 
   python manage.py migrate
6. create admin user
    ```bash
   python manage.py createsuperuser
7. python manage.py createsuperuser
    ```bash
   python manage.py runserver


    
