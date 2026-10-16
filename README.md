# SAT × AI

**A Smarter Way to Practice for the SAT**

## Description

SAT × AI is a web application built with Django to help students
practise SAT-style questions, review their performance, and get
additional help from an AI assistant.

I started this project primarily to **learn backend development** by
building a complete application rather than only following isolated
tutorials. I worked on the backend with Python and Django, including
application logic, database models, forms, views, URLs, user accounts,
practice sessions, and AI API integration.

For the frontend, I used a **vibe-coding approach**: I used AI
assistance to help create and refine the interface, using Django
templates, HTML, Bootstrap, and JavaScript. This let me focus more of my
learning on understanding how the backend works and how the frontend
communicates with it.

## Features

### SAT practice

-   Choose practice settings such as subject, domain, difficulty, number
    of questions, and time limit.
-   Practise questions from Reading and Writing and Math.
-   Support for multiple-choice and fill-in-the-blank questions,
    depending on the question.
-   Navigate questions during a practice session.
-   Review answers after completing a session.
-   View results such as correct answers, incorrect answers, unanswered
    questions, and accuracy.

### Question categories

**Reading and Writing** - Information and Ideas - Craft and Structure -
Expression of Ideas - Standard English Conventions

**Math** - Algebra - Advanced Math - Problem-Solving and Data Analysis -
Geometry and Trigonometry

### AI assistant

-   Google Gemini API integration for AI-assisted question support.
-   Send a question, an answer, or a follow-up prompt to request further
    explanation.
-   Designed to help users understand the reasoning behind an answer.

AI responses may be inaccurate or unavailable, depending on the model
and API service.

### User accounts

-   User registration and login.
-   User-specific practice records.
-   Profile and account-management features.

### Error pages

Custom templates for common HTTP errors, including 400, 403, 404, and
500.

## Tools

  Python                              Backend programming language

  Django                              Web framework, request handling,
                                      authentication, and application
                                      logic

  Django ORM                          Database queries and model
                                      operations

  SQLite                              Development database

  HTML and Django Templates           Page structure and dynamic content

  Bootstrap 5                         Frontend layout and UI components

  JavaScript                          Interactive browser-side behaviour
                                      and AI chat requests

  Google Gemini API                   AI-powered assistance

  JSON                                Storing and importing question data

**Frontend note:** The frontend was developed with AI assistance using a
vibe-coding workflow. The main learning focus of this project is backend
development.

## Project Structure

``` text
SAT-x-AI/
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core/
│   ├── migrations/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── psai_project/
│   └── Django project configuration
├── static/
├── templates/
│   ├── 400.html
│   ├── 403.html
│   ├── 404.html
│   └── 500.html
├── .env                    # Local secrets; do not commit
├── .gitignore
├── db.sqlite3              # Local development database
├── manage.py
├── README.md
├── requirements.txt
└── sat_questions.json      # Contain SAT practice questions created by ChatGPT 
```

### Main apps

-   **`accounts/`** --- user authentication, account forms, and
    account-related views.
-   **`core/`** --- SAT questions, practice sessions, results, and
    AI-related functionality.
-   **`psai_project/`** --- project-level Django configuration,
    including settings and root URL routing.
-   **`static/`** --- static assets such as CSS.
-   **`templates/`** --- shared templates and custom error pages.
-   **`core/services.py`** --- service/helper logic used by the core
    application.

## Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the URL and directory name with your actual GitHub repository
details.

### 2. Create and activate a virtual environment

On macOS or Linux:

``` bash
python3 -m venv psai_env
source psai_env/bin/activate
```

### 3. Install dependencies

If the repository includes a `requirements.txt` file:

``` bash
pip install -r requirements.txt
```

If it does not, install the dependencies required by the project. You
can create a dependency file from your working environment with:

``` bash
pip freeze > requirements.txt
```

Review the generated file before committing it.

### 4. Configure environment variables

Create a `.env` file in the project root and set the Gemini API key
using the variable name expected by your settings. For example:

``` dotenv
GEMINI_API_KEY=your_gemini_api_key_here
```

Make sure your Django settings load the environment variable correctly.
Never commit your real API key or other secrets to GitHub.

### 5. Apply migrations

``` bash
python manage.py migrate
```

### 6. Create an admin user (optional)

``` bash
python manage.py createsuperuser
```

### 7. Start the development server

``` bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Question Data

The SAT question dataset is stored in JSON format. The questions were
**created with ChatGPT** and are intended for practice and learning.
They should be reviewed for correctness and quality; AI-generated
content can contain errors.

### Import JSON questions using Django shell

1.  Put the JSON file in the project root, next to `manage.py`.
2.  Make sure its structure matches the fields in your `Question` model.
3.  Run Django shell:

``` bash
python manage.py shell
```

4.  In the Django shell, run the following example. Change the filename
    and fields to match your actual dataset and model:

``` python
import json
from pathlib import Path
from core.models import Question

json_path = Path("sat_easy_questions_400.json")

with open(json_path, 'r') as file:
    data = json.load(file)

questions = []

for item in data:
    questions.append(Question(**item))

Question.objects.bulk_create(questions)

print(f"Imported {len(questions)} questions.")
```

Exit the shell when finished:

``` python
exit()
```


## Purpose

I created SAT × AI to learn backend development by building something
practical. Instead of studying Django concepts separately, I used them
to solve real application problems: storing questions, filtering them
for practice, managing user sessions, saving answers, calculating
results, and connecting an external AI service.

The project also gives me a place to practise integrating different
parts of a web application into one working system.

## What I've Learned

Through building this project, I have been learning and practising:

-   **Django project structure:** separating functionality into apps and
    organizing URLs, views, forms, models, and templates.
-   **Request and response flow:** handling GET and POST requests,
    validating submitted forms, redirecting users, and rendering pages.
-   **Database design:** defining models and relationships and using
    migrations to evolve the database.
-   **Django ORM:** filtering, excluding, ordering, counting, and
    retrieving records without writing every query in SQL.
-   **Authentication and authorization:** protecting views and
    connecting application data to individual users.
-   **Practice-session logic:** selecting questions, saving answers,
    handling unanswered questions, and calculating results.
-   **JSON and data import:** reading structured files with Python and
    creating database records.
-   **API integration:** sending requests to the Gemini API and handling
    responses and errors.
-   **Frontend/backend communication:** using JavaScript to send data to
    Django endpoints and display returned results.
-   **Debugging:** reading tracebacks, investigating errors, and
    improving the application step by step.
-   **AI-assisted development:** using AI to help build the frontend
    while learning to inspect, understand, test, and revise the
    generated code.

This project is a work in progress, so the list reflects skills I am
practising and developing rather than a claim of mastery.

## Disclaimer

SAT × AI is an independent educational project. It is **not affiliated
with, endorsed by, or sponsored by the College Board**. SAT is a
trademark of the College Board.

The practice questions were created with ChatGPT and are not official
College Board questions. AI-generated questions and explanations may
contain errors, so users should verify them against trusted study
resources.
