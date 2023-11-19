# Daily_Task_Scheduler


## What is Daily Task Scheduler?
  
  This is an application where we can schedule our regular tasks, which can be rescheduled by the way as well as mark as Completed if in case that specific task is completed. And also an email alert is auto enabled and gets triggered whenever the task gets rescheduled.

## Setup
  In Order to keep this application running we must install few libraries in python.. Which are the following ones:-
    1. flask
    2. flask_login
    3. sqlite3
    4. email
    5. werkzeug
    6. smtplib


   **Steps:-**
     1. Setup of virtual env:-
          Create a virtual environment just to keep it from colliding from the existing libraries and their versions in the system.
  
     2. So, to install all these libraries, open the terminal and go to the folder in which requirements.txt exists and use the following command.
               pip install -r requirements.txt

## Once the setup is done, go to the folder where app.py is situated.. And run the app.py file..

     This starts the development server at the local host. So that's how you can get the app running in your browser..

## If you are a user trying to access it for the first time try to register before you login..

## Once registered and logged in.. Then you will be prompted to the home page where when the events or tasks are added will be displayed..
    So try adding an event, modifying it or deleting it on completion..



## Future Scope & Reference:-

  This can be further added with many features by integrating with the calendar directly on the system so that we can get a direct remainder always.. And also adding dashboards so that we can track daily progress of how it is going and how can this be changed or how dedicative we should become likewise..
