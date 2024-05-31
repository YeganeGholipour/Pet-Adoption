# Pet Adoption API

Welcome to the Pet Adoption API! This project is built using Django Rest Framework and allows users to manage pet adoptions.

## Features

- **Authentication**: Users can sign up, sign in, and sign out securely.
- **CRUD Operations**: Easily create, read, update, and delete pet adoptions.
- **Filtering and Searching**: Filter and search for pets based on various criteria.
- **Dockerized**: The project comes with Docker and Docker Compose configuration files for easy deployment.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/pet-adoption-api.git
```

2. Navigate to the project directory:

```bash
cd pet-adoption-api
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run database migrations:

```bash
python manage.py migrate
```

5. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

