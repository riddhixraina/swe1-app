# swe1-app

[![Build Status](https://app.travis-ci.com/riddhixraina/swe1-app.svg?branch=main)](https://app.travis-ci.com/riddhixraina/swe1-app)
[![Coverage Status](https://coveralls.io/repos/github/riddhixraina/swe1-app/badge.png?branch=main)](https://coveralls.io/github/riddhixraina/swe1-app?branch=main)

A Django polls application with continuous integration, automated testing, and AWS deployment.

## Features

- View Polls: Users can see a paginated list of all available poll questions
- Vote: Users can select a choice for a specific poll question and cast their vote
- View Results: After voting, users can see the aggregated results for the poll
- Admin Interface: Complete admin backend for managing polls
- Responsive UI: Clean and simple interface

## CI/CD Pipeline

- **Travis CI**: Automated builds on every push and pull request
- **Black**: Code formatting validation
- **Flake8**: Linting and code quality checks
- **Coverage**: 100% test coverage
- **Coveralls**: Coverage reporting and tracking
- **AWS Elastic Beanstalk**: Automated deployment on successful builds

## Local Development

### Prerequisites

- Python 3.8+
- pip and virtualenv
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/riddhixraina/swe1-app.git
cd swe1-app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit http://127.0.0.1:8000/polls/ to see the application.

## Running Tests

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report

# Check code formatting
black --check .

# Run linter
flake8 .
```

## Deployment

The application is automatically deployed to AWS Elastic Beanstalk when:
- All tests pass
- Code passes black formatting check
- Code passes flake8 linting check
- Changes are pushed to the `main` branch

**Live Application:** http://swe1-app-env.eba-ugzpcmix.us-west-2.elasticbeanstalk.com/polls/

## Technologies Used

- **Backend**: Django (Python)
- **Database**: SQLite (development), PostgreSQL (production)
- **CI/CD**: Travis CI
- **Deployment**: AWS Elastic Beanstalk
- **Testing**: Django TestCase, Coverage.py
- **Code Quality**: Black, Flake8

## License

This project was created as part of a software engineering course assignment.
