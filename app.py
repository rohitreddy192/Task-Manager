from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import datetime
from flask import request, jsonify
from email_alert import send_email
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ... Existing imports ...
#Creating Database
def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    duration INTEGER NOT NULL,
                    notes TEXT,
                    completed INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()
#Declaring the flask application 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with your own secret key
app.config['SESSION_TYPE'] = 'filesystem'

#Declaring a Login Manager to take care of our login sessions
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password

users = {'user_id_here':  User('user_id_here', 'password')}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

#Login Route --> This is the first page to open when user didnot login.. Any other pages other than this requires login so user comes here at first.
@app.route('/login', methods=['GET', 'POST'])
def login():
    global users
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        # Retrieve user data from the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id, username, password FROM users WHERE username=?", (user_id,))
        user_data = c.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[2], password):
            session['user_id'] = user_id
            users[user_data[1]] = User(user_data[1], user_data[2])
            login_user(users[user_data[1]])
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')

#Log Out Route 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Clear the entire session to log the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

#SignUp 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        # Insert user data into the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=?", (user_id,))
        record = c.fetchone()
        if len(record) > 0:
            flash('Username already exists please try a new one.','failed')

            return render_template('signup.html', flashmessage = 'Username already exists please try a new one.')
        
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user_id, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')


#This is the home page and our dashboard page where our tasks scheduled are appeared.. 
@app.route('/')
@login_required
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events WHERE completed = 0 ORDER BY date, time")
    tasks = c.fetchall()
    conn.close()
    
    current_date_and_time = datetime.datetime.now() 
    tasks = [(task[0], task[1], datetime.datetime.strptime(task[2], '%Y-%m-%d'), task[3], task[4], task[5], task[6]) for task in tasks]
    for task in tasks: 
        if task[2] < current_date_and_time < task[2] + datetime.timedelta(hours=task[4]) and not task[6]:
            send_email(to_email='vinay.padala2000@gmail.com', subject = 'Reminder: You have a task "{}" scheduled now.'.format(task[1]), message='You may reschedule or cancel it logging in!!!')

    return render_template('index.html', tasks=tasks,  current_date_and_time=current_date_and_time)

#When we want to add a new task and on clicking Add Event Button this triggers.. 
@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        task_name = request.form['task_name']
        date = request.form['date']
        time = request.form['time']
        duration = request.form['duration']
        notes = request.form['notes']  # New field for notes
        completed = 0

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO events (task_name, date, time, duration, notes, completed) VALUES (?, ?, ?, ?, ?, ?)",
                  (task_name, date, time, duration, notes, completed))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_event.html')

def create_connection():
    return sqlite3.connect('tasks.db')

#When we want to get the details of a task we fetch the information as follows using task_id
@app.route('/get_task_details/<int:task_id>', methods=['GET'])
@login_required
def get_task_details(task_id):
    try:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        # Query the database to fetch task details based on the task_id
        cursor.execute("SELECT id, task_name, date, time, duration, notes FROM events WHERE id = ?", (task_id,))
        task_details = cursor.fetchone()

        if task_details:
            # Convert the task details to a dictionary and return as JSON response
            task_dict = {
                "id": task_details[0],
                "name": task_details[1],
                "date": task_details[2],
                "time": task_details[3],
                "duration": task_details[4],
                "notes": task_details[5]
            }
            return jsonify(task_dict)
        else:
            # Return a 404 error if the task is not found
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()    

#When edit task is clicked it gives this function some work to do.. so any new edits are updated.. 
@app.route('/edit_task', methods=['POST'])
@login_required
def edit_task():
    if request.method == 'POST':
        try:
            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            
            # Parse JSON data from the request
            edited_task = request.json

            # Update the task in the database with the edited values
            cursor.execute("UPDATE events SET task_name = ?, date = ?, time = ?, duration = ?, notes = ? WHERE id = ?",
                           (edited_task["name"], edited_task["date"], edited_task["time"],
                            edited_task["duration"], edited_task["notes"], edited_task["id"]))
            conn.commit()

            # Check if any rows were affected (successful update)
            if cursor.rowcount > 0:
                return jsonify({"message": "Task updated successfully"})
            else:
                return jsonify({"error": "Task not found"}), 404
        except Exception as e:
            print(str(e))
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()

#When we click on reschedule this is the place where it gets updated.. 
@app.route('/reschedule_task', methods=['POST'])
@login_required
def reschedule_task():
    try:
        # Get data from the request
        data = request.get_json()

        # Extract task_id, newDate, and newTime from the JSON data
        task_id = data.get('task_id')
        new_date = data.get('newDate')
        new_time = data.get('newTime')

        # Create a connection to the SQLite database
        conn = create_connection()
        cursor = conn.cursor()

        # Update the task's date and time in the database
        cursor.execute("UPDATE events SET date=?, time=? WHERE id=?", (new_date, new_time, task_id))
        cursor.execute("Select * from events where id = ?",(task_id,))
        records = cursor.fetchone()
        conn.commit()

        # Check if any rows were affected (task with given id exists)
        if cursor.rowcount > 0:
            conn.close()
            return jsonify({'message': 'Task rescheduled successfully'}), 200
        else:
            conn.close()
            return jsonify({'message': 'Task not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
#Upon clicking completed on the frontend.. the task_id is marked to completed in the backend here.. 
@app.route('/mark_completed/<int:task_id>', methods=['POST'])
@login_required
def mark_completed(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE events SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return '', 204


if __name__ == "__main__":
    create_database()
    app.run(debug=True)