
# AI-Enabled Structural Health Monitoring for Smart Infrastructure

## Project Overview

This AI-driven project addresses the critical need for real-time monitoring of infrastructural health in bridges, buildings, and industrial frameworks. Structural failures can lead to catastrophic consequences — both economically and in terms of human safety.

### Why It's Necessary

- Aging infrastructure and increasing urbanization require proactive safety solutions.
- Manual inspections are slow, infrequent, and subjective.
- Real-time anomaly detection enables predictive maintenance and disaster prevention.

### How We Tackle the Problem

- Deploying multi-sensor networks to collect structural parameters continuously.
- Applying AI/ML models to detect early warning signs of structural deterioration.
- Storing, analyzing, and visualizing data via an intuitive web dashboard.
- Integrating chatbot support for user-friendly interaction and status updates.

## Features

- Real-time data visualization from sensors
- AI anomaly detection and predictive alerts
- User registration, login, and authentication system
- Chatbot for interacting with the system via natural language
- SQLite database for persistent data storage
- Modular Flask backend with API endpoints
- Responsive frontend using Chart.js and HTML/CSS

## Technologies Used

- **Python 3.10+**
- **Flask (Web Framework)**
- **Flask SQLAlchemy (ORM for SQLite)**
- **Chart.js (Graph rendering)**
- **HTML5/CSS3/JavaScript**
- **SQLite (Lightweight database)**
- **Pandas & NumPy (Data handling)**
- **scikit-learn (AI/ML logic)**

## Installation & Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/Feroan101/AI-Enabled-Structural-Health-Monitoring
    cd ai-enabled-shm
    ```

2. Create and activate a Python virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate        # Windows: venv\Scripts\activate
    ```

3. Install dependencies using `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database:

    ```bash
    sqlite3 shm_web.db < user_data.sql
    ```

5. Run the Flask application:

    ```bash
    python app.py
    ```

6. Open your browser and go to:

    ```
    http://localhost:5000
    ```
