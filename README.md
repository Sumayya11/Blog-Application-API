# Task2

# Flask-JWT-Post-Comment-App

This is a Flask application with user authentication, post creation, and commenting features. The application uses JWT (JSON Web Tokens) for user authentication and Flask-SQLAlchemy for interacting with a PostgreSQL database.

## Prerequisites

Make sure you have Python and pip installed on your system.

## Configuration
Update the app.config['SQLALCHEMY_DATABASE_URI'] in app.py with your PostgreSQL database URI.

## API Endpoints
--   POST /api/signup: Create a new user.
--   POST /api/login: Authenticate and obtain a JWT token.
--   POST /api/post: Create a new post.
--   POST /api/comment: Post a comment on a specific post.

Refer to the app.py file for more details on the API endpoints and request payloads.
