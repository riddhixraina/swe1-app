# swe1-app

# SWE-1 Polls Application

This is a simple polls application built with Django as part of a software engineering course assignment. The project follows the official Django tutorial (Parts 1-4) to create a functional web application where users can view, vote on, and see the results of various polls.

**Live, deployed application:**  
`http://<your-app-env>.elasticbeanstalk.com/polls`

---

## Features

- **View Polls:** Users can see a paginated list of all available poll questions.
- **Vote:** Users can select a choice for a specific poll question and cast their vote.
- **View Results:** After voting, users can see the aggregated results for the poll.
- **Admin Interface:** A complete admin backend (`/admin`) allows for the creation, modification, and deletion of polls and choices.
- **Responsive UI:** The application has a clean and simple interface that works on different screen sizes.

---

## Technology Stack

- **Backend:** Python with the Django Framework
- **Database:** SQLite (for local development)
- **Frontend:** HTML5 with inline CSS for styling
- **Deployment:** AWS Elastic Beanstalk

---

## Local Development Setup

To run this project on your local machine, follow these steps:

### Prerequisites

- Python 3.8+
- `pip` and `venv`

### Clone the Repository

```bash
git clone https://github.com/riddhixraina/swe1-app.git
cd swe1-app
```

### Create and Activate a Virtual Environment

```bash
# Create the environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Database Migrations

```bash
python manage.py migrate
```

### Create an Admin Superuser

```bash
python manage.py createsuperuser
```
_Follow the prompts to create your admin account._

### Run the Development Server

```bash
python manage.py runserver
```

The application will be available at [http://127.0.0.1:8000/polls/](http://127.0.0.1:8000/polls/).

---

## Deployment

This application is configured for deployment to **AWS Elastic Beanstalk**.  
The necessary configuration files are located in the `.ebextensions` directory.  
The `django.config` file sets the required environment variables for the WSGI path and Django settings module.

---
