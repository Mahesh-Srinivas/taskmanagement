from flask import Flask, render_template, session, redirect, request, flash, url_for, jsonify
import sqlite3
import secrets
from datetime import datetime
from math import ceil
import math



app = Flask(__name__)

# Generate a random secret key
secret_key = secrets.token_hex(16)  # Generate a random 32-character hexadecimal string

# Set the secret key for the session
app.secret_key = secret_key

# Route for Home page

@app.route("/")
def home():
    # Set the title for the home page
    title = 'Home'
    # Render the 'index.html' template with the title variable
    return render_template('index.html', title=title)

# Route for login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform user authentication
        username = request.form['username']
        password = request.form['password']

        # Connect to the SQLite database
        conn = sqlite3.connect('static/DB/Project_Management_System.db')
        cursor = conn.cursor()

        # Execute a query to check the username and password
        query = "SELECT * FROM Users WHERE UserName = ? AND Password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            # If authentication is successful, store user data in the session
            session['username'] = user[0]  # Assuming the username is in the first column
            session['logged_in'] = True
            conn.close()
            return redirect('/dashboard')

        # Authentication failed, show error message
        error_message = 'Invalid username or password'
        conn.close()
        return render_template('login.html', error_message=error_message)

    return render_template('login.html')


# Route for registration page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input from the registration form
        username = request.form['username']
        password = request.form['password']

        # Connect to the SQLite database
        conn = sqlite3.connect('static/DB/Project_Management_System.db')
        cursor = conn.cursor()

        # Check if the username is already taken
        query = "SELECT * FROM Users WHERE UserName = ?"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Username is already taken, show error message
            error_message = 'Username already taken'
            conn.close()
            return render_template('register.html', error_message=error_message)

        # Insert new user into the database
        query = "INSERT INTO Users (UserName, Password) VALUES (?, ?)"
        cursor.execute(query, (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# Route for dashboard page
@app.route("/dashboard")
def dashboard():
    # Check if the user is logged in
    if session.get('logged_in'):
        username = session.get('username')
        
        # Fetch data from the database
        conn = sqlite3.connect('static/DB/Project_Management_System.db')
        cursor = conn.cursor()

        # Get the number of tasks for the user
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE UserName=?", (username,))
        num_tasks = cursor.fetchone()[0]

        # Get the number of to-do lists for the user
        cursor.execute("SELECT COUNT(*) FROM ToDo WHERE UserName=?", (username,))
        num_todolists = cursor.fetchone()[0]

        # Get the number of teams for the user
        cursor.execute("SELECT COUNT(*) FROM teams WHERE UserName=?", (username,))
        num_teams = cursor.fetchone()[0]

        # Get the number of projects for the user
        cursor.execute("SELECT COUNT(*) FROM projects WHERE UserName=?", (username,))
        num_projects = cursor.fetchone()[0]

        conn.close()

        return render_template('dashboard.html', username=username, num_tasks=num_tasks, num_todolists=num_todolists, num_teams=num_teams, num_projects=num_projects)
    else:
        # User is not logged in, redirect to login page
        return redirect('/login')


# Route for ToDo page
@app.route("/todo", methods=["GET", "POST"])
def todo():
    # Check if the user is logged in
    if session.get('logged_in'):
        # Get the username from the session
        username = session.get('username')

        # Connect to the SQLite database
        conn = sqlite3.connect('static/DB/Project_Management_System.db')
        cursor = conn.cursor()

        # Get the page number from the query parameters
        page = request.args.get('page', 1, type=int)
        rows_per_page = 6

        # Calculate the offset for pagination
        offset = (page - 1) * rows_per_page

        # Execute the SQL query to retrieve todo items for the logged-in user with pagination
        cursor.execute('SELECT * FROM todo WHERE UserName = ? LIMIT ? OFFSET ?',
                       (username, rows_per_page, offset))
        rows = cursor.fetchall()

        # Count the total number of rows for the logged-in user
        cursor.execute('SELECT COUNT(*) FROM todo WHERE UserName = ?', (username,))
        total_rows = cursor.fetchone()[0]

        # Calculate the total number of pages based on the total rows and rows per page
        total_pages = ceil(total_rows / rows_per_page)

        # Close the database connection
        conn.close()

        if request.method == "POST":
            # Get the form data
            title = request.form.get("todotitle")
            description = request.form.get("tododesc")
            date = datetime.now().strftime("%Y-%m-%d")

            # Connect to the SQLite database
            conn = sqlite3.connect('static/DB/Project_Management_System.db')
            cursor = conn.cursor()

            # Execute the SQL query to insert the new task into the todo table
            cursor.execute('INSERT INTO todo (UserName, title, Description, Date) VALUES (?, ?, ?, ?)',
                           (username, title, description, date))
            conn.commit()

            # Close the database connection
            conn.close()

            flash("Task added successfully", "success")

            # Redirect to the ToDo page with the current page number
            return redirect(url_for('todo', page=page))

        # Render the template and pass the username, rows, total_pages, and current page to it
        return render_template('todo.html', username=username, rows=rows, total_pages=total_pages, page=page)

    else:
        # User is not logged in, redirect to the login page
        return redirect('/login')


# Route for marking a task as done
@app.route('/mark_done/<int:task_id>', methods=['POST'])
def mark_done(task_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('static/DB/Project_Management_System.db')
    cursor = conn.cursor()

    # Update the task status as done in the database
    cursor.execute('UPDATE todo SET Status = ? WHERE ID = ?', ('Done', task_id))
    conn.commit()

    # Close the database connection
    conn.close()

    # Return a JSON response indicating success
    return jsonify({'success': True})



# Route for deleting a task
@app.route('/delete_task', methods=['POST'])
def delete_task():
    # Get the task ID from the request form data
    task_id = request.form.get('task_id')

    # Connect to the SQLite database
    conn = sqlite3.connect('static/DB/Project_Management_System.db')
    cursor = conn.cursor()

    # Delete the task from the database
    cursor.execute('DELETE FROM todo WHERE id = ?', (task_id,))
    conn.commit()

    # Close the database connection
    conn.close()

    # Return a JSON response indicating success
    return jsonify({'success': True})

# Route for changing password
@app.route("/changepasswd", methods=['GET', 'POST'])
def changepassword():
    # Check if the user is logged in
    if session.get('logged_in'):
        username = session.get('username')

        if request.method == 'POST':
            # Get the new password from the form
            new_password = request.form['password']

            # Update the password in the database
            conn = sqlite3.connect('static/DB/Project_Management_System.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute("UPDATE Users SET password = ? WHERE UserName = ?", (new_password, username))
                conn.commit()
                flash("Password changed successfully!", "success")
            except Exception as e:
                flash("An error occurred. Please try again later.", "danger")
                print(e)
            finally:
                conn.close()

            return redirect('/changepasswd')  # Redirect to the same page after updating the password

        return render_template('passwd.html', username=username)

    else:
        # User is not logged in, redirect to login page
        return redirect('/login')

#  Route for Projects
@app.route('/project', methods=['GET', 'POST'])
def project():
    # Check if the user is logged in
    if session.get('logged_in'):
        username = session.get('username')
        
        if request.method == 'POST':
            conn = sqlite3.connect('static/DB/Project_Management_System.db')
            cursor = conn.cursor()
            name = request.form['name']
            description = request.form['description']
            cursor.execute("INSERT INTO projects (UserName, name, description) VALUES (?, ?, ?)",
               (session['username'], name, description))

            conn.commit()
            conn.close()
            return redirect(url_for('project'))
        
        # Fetch data from the database
        conn = sqlite3.connect('static/DB/Project_Management_System.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE username=?", (username,))
        projects = cursor.fetchall()
        conn.close()

        # Calculate total pages (assuming 10 projects per page)
        total_projects = len(projects)
        projects_per_page = 10
        total_pages = math.ceil(total_projects / projects_per_page)

        return render_template('project.html', username=username, projects=projects, total_pages=total_pages)
    else:
        # User is not logged in, redirect to login page
        return redirect('/login')


# Route for Tasks

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    # Check if the user is logged in
    if session.get('logged_in'):
        username = session.get('username')

        if request.method == 'POST':
            conn = sqlite3.connect('static/DB/Project_Management_System.db')
            cursor = conn.cursor()
            taskName = request.form['taskName']
            taskDesc = request.form['taskDesc']
            cursor.execute("INSERT INTO tasks (UserName, taskName, taskDesc) VALUES (?, ?, ?)",
                           (session['username'], taskName, taskDesc))
            conn.commit()
            conn.close()
            return redirect(url_for('tasks'))

        # Fetch data from the database
        conn = sqlite3.connect('static/DB/Project_Management_System.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE UserName=?", (username,))
        tasks = cursor.fetchall()
        conn.close()

        # Calculate total pages (assuming 10 tasks per page)
        tasks_per_page = 10
        total_tasks = len(tasks)
        total_pages = math.ceil(total_tasks / tasks_per_page)

        # Implement Round Robin for pagination
        page = int(request.args.get('page', 1))  # Get current page number from request query parameters
        start_index = (page - 1) * tasks_per_page
        end_index = start_index + tasks_per_page
        paginated_tasks = tasks[start_index:end_index]

        return render_template('tasks.html', username=username, tasks=paginated_tasks, total_pages=total_pages, page=page)
    else:
        # User is not logged in, redirect to login page
        return redirect('/login')

# Route for Teams
@app.route('/teams', methods=['GET', 'POST'])
def teams():
    # Check if the user is logged in
    if session.get('logged_in'):
        username = session.get('username')

        if request.method == 'POST':
            conn = sqlite3.connect('static/DB/Project_Management_System.db')
            cursor = conn.cursor()
            teamName = request.form['teamName']
            teamDesc = request.form['teamDesc']
            teamMembers = request.form['teamMembers']
            cursor.execute("INSERT INTO teams (UserName, teamName, teamDesc, teamMembers) VALUES (?, ?, ?, ?)",
                           (session['username'], teamName, teamDesc, teamMembers))
            conn.commit()
            conn.close()
            return redirect(url_for('teams'))

        # Fetch data from the database
        conn = sqlite3.connect('static/DB/Project_Management_System.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teams WHERE UserName=?", (username,))
        teams = cursor.fetchall()
        conn.close()

        # Calculate total pages (assuming 10 teams per page)
        total_teams = len(teams)
        teams_per_page = 10
        total_pages = math.ceil(total_teams / teams_per_page)

        return render_template('teams.html', username=username, teams=teams, total_pages=total_pages)
    else:
        # User is not logged in, redirect to login page
        return redirect('/login')


# Route for logging out
@app.route("/logout")
def Logout():
    # Clear the session data
    session.clear()
    return redirect('/login')


# 404 Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
