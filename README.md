# Daily_Task_Scheduler


What is Daily Task Scheduler?
  This is an application where we can schedule our regular tasks, which can be rescheduled by the way as well as mark as Completed if in case that specific task is completed. And also an email alert is auto enabled and gets triggered whenever the task gets rescheduled.

1. Setup
  In Order to keep this application running we must install few libraries in python.. Which are the following ones:-
    a. flask
    b. flask_login
    c. sqlite3
    d. email
    e. werkzeug
    f. smtplib


   Steps:-
   1. Setup of virtual env:-
        Create a virtual environment just to keep it from colliding from the existing libraries and their versions in the system.
  
   2. So, to install all these libraries, open the terminal and go to the folder in which requirements.txt exists and use the following command.
  
             pip install -r requirements.txt

2. Once the setup is done, go to the folder where app.py is situated.. And run the app.py file..

     This starts the development server at the local host. So that's how you can get the app running in your browser..

3. If you are a user trying to access it for the first time try to register before you login..

4. Once registered and logged in.. Then you will be prompted to the home page where when the events or tasks are added will be displayed..
    So try adding an event, modifying it or deleting it on completion..



Future Scope & Reference:-

1. This can be further added with many features by integrating with the calendar directly on the system so that we can get a direct remainder always.. And also adding dashboards so that we can track daily progress of how it is going and how can this be changed or how dedicative we should become likewise..
