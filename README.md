# Task Manager Application with Flask


## What is this Application?
  
  This is a Task Manager application built using Flask, allowing users to manage their tasks, schedule events, and set reminders.


## Introduction
  This Flask-based Task Manager application allows users to perform various task-related operations. Users can register, log in, add, edit, delete, and mark tasks as completed. It also sends reminders for scheduled tasks via email.

## Features
  -**User Authentication:** Users can sign up and log in securely.
  -**Task Management:** Add, edit, delete, and mark tasks as completed.
  -**Email Reminders:** Sends reminders for scheduled tasks via email.
  -**Responsive UI:** User-friendly interface for managing tasks.
  -**Database:** SQLite database used to store user data and task details.

## Installation
### 1. Clone the repository:
    git clone https://github.com/rohitreddy192/Daily_Task_Scheduler.git
### 2. Navigate to the project directory:
    cd Daily_Task_Scheduler
### 3. Install Dependencies:
    pip install -r requirements.txt
### 4. Database Setup:
    - Run create_database() function to initialize the SQLite database.
    
## Usage
### 1. Run Application:
     python app.py
### 2. Access the Application:
    - Open a web browser and go to http://localhost:5000 to access the Task Manager application.
### 3. Functionalities:
    - Register or log in to manage tasks.
    - Add, edit, delete tasks, and mark them as completed.
    - Receive email reminders for scheduled tasks.
## Technologies Used
  - Flask
  - SQLite
  - HTML/CSS
  - JavaScript
  - Python 3.x

## File Structure
├── app.py                  # Main Flask application file
├── tasks.db                # SQLite database file
├── email_alert.py          # Email alert functionality
├── static/
│   ├── css/
│   │   └── styles.css       # CSS stylesheets
└── templates/
    ├── add_event.html       # HTML templates for different routes
    ├── index.html           
    ├── login.html           
    ├── signup.html


## Future Scope & Reference:-

  This can be further added with many features by integrating with the calendar directly on the system so that we can get a direct remainder always.. 

## Contributions
  Contributions are welcome! If you'd like to contribute to this project, feel free to create issues or pull requests.
