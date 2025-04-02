```markdown
# api_online_shop_v1
This project is an implementation of an API for an online store built with Django and Django REST Framework. It includes functionality for user registration and authentication, product management, shopping cart, and order handling.

## Features

- User registration and authentication via email and password.
- Create, view, update, and delete products.
- Add products to the shopping cart.
- Place an order.
- Authentication via JWT (JSON Web Tokens).
- API documentation using Swagger.

## Technologies

- Django 5.1.7
- Django REST Framework
- PostgreSQL
- Simple JWT (JSON Web Tokens)

## How to Run the Project

### 1. Clone the repository

Clone the repository to your local machine:

```bash
git clone https://github.com/UaBogdan2004/online-shop-api.git
cd online-shop-api
```

### 2. Install dependencies

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # For Linux/MacOS
.venv\Scripts\activate  # For Windows
```

Install the dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Database Setup

1. Create a `.env` file in the root directory of the project.
2. Add the following variables to the `.env` file:

```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
EMAIL_HOST_PASSWORD=your_email_password
```

3. Ensure that the `settings.py` file is configured to read these values using `python-decouple`:

```python
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'PORT': config('DB_PORT'),
        'HOST': config('DB_HOST'),
    }
}
```

### 4. Database Migrations

Run the migrations to create the database tables:

```bash
python manage.py migrate
```

### 5. Create a Superuser

To access the Django admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

### 6. Start the Server

Run the Django server:

```bash
python manage.py runserver
```

Now, you can access the API at `http://127.0.0.1:8000/`.

### 7. API Documentation

- Swagger documentation is available at: `http://127.0.0.1:8000/swagger/`
## Author

- **Bogdan** (https://github.com/UaBogdan2004)

## License

This project is licensed under the BSD License.
