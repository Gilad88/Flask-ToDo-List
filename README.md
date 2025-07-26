# Flask ToDo App with Docker Compose

## Overview
This is a simple full-stack ToDo list web application designed to demonstrate modern web development practices using Python Flask, PostgreSQL, and Docker. It allows users to manage their daily tasks efficiently.

## Features
The application provides the following core functionalities:
* Display a list of all ToDo items.
* Create and add new ToDo items.
* Mark a ToDo item as complete or incomplete.
* Edit the content of an existing ToDo item.
* Delete a ToDo item.
* Mark all ToDo items as completed with a single click.
* Tasks are displayed with their creation timestamp.

## Technologies Used
* **Backend:** Python 3.10+, Flask
* **Database:** PostgreSQL 15+
* **Containerization:** Docker, Docker Compose
* **Frontend:** HTML5, CSS3, Bootstrap 5 (or 4, specify which one), jQuery
* **Version Control:** Git, GitHub

## Local Setup / Getting Started

To run this application locally, you need to have Docker Desktop (which includes Docker Compose) installed on your system.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Gilad88/Flask-ToDo-List.git](https://github.com/Gilad88/Flask-ToDo-List.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd Flask-ToDo-List
    ```
3.  **Build and run the Docker containers:**
    This command will build the Flask application image, set up the PostgreSQL database, and start both services.
    ```bash
    docker compose up -d --build
    ```
    *The first time you run this, it might take a few minutes to download images and build.*

4.  **Access the application:**
    Open your web browser and go to:
    ```
    http://localhost:5000
    ```

5.  **Cleaning up (Optional):**
    To stop and remove the running containers and delete the database volume (all data will be lost):
    ```bash
    docker compose down -v
    ```

## Project Structure
* `app.py`: The main Flask application file, containing routes, database models, and application logic.
* `init_db.py`: A script to initialize the database schema (create tables).
* `requirements.txt`: Lists all Python dependencies.
* `Dockerfile`: Defines how the Flask application's Docker image is built.
* `docker-compose.yml`: Orchestrates the multi-container Docker application (Flask app and PostgreSQL database).
* `templates/`: Contains Jinja2 HTML templates (`index.html`, `base.html`, `update.html`).
* `static/`: Contains static assets like CSS files (`static/css/style.css`).

## Contributing
(Optional: Add guidelines if you plan to accept contributions)

## License
(Optional: Add your project's license, e.g., MIT License)
