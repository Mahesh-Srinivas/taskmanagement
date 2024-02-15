# Project Management System

This is a web-based project management system built using Flask, SQLite, and Bootstrap. The system allows users to manage tasks, to-do lists, projects, and teams. Users can register an account, log in, and perform various operations such as creating tasks, adding to-do lists, managing projects, and collaborating with team members.

## Features

- User authentication: Users can register an account and log in to access the system.
- Task Management: Users can create and manage tasks.
- To-Do Lists: Users can create and manage to-do lists.
- Project Management: Users can create and manage projects.
- Team Collaboration: Users can create teams and collaborate with team members.
- Password Change: Users can change their passwords.
- Responsive Design: The system is built with a responsive design using Bootstrap.

## Prerequisites

- Python 3.x
- Flask
- SQLite

## Installation

Clone the repository:

```bash
git clone <repository_url>
```

Change into the project directory:

```bash
cd Project_Management_System
```

Create a virtual environment (optional):

```bash
python3 -m venv venv
```

Activate the virtual environment (optional):

> For Windows:

```bash
venv\Scripts\activate
```

For Unix/macOS:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Initialize the database:

```bash
python init_db.py
```

Start the application:

```bash
python app.py
```

Open a web browser and visit **[http://localhost:5000](http://localhost:5000)** to access the application.

## Screenshots

### Home Page

![Home](ss/home.png)

### Login Page

![Home](ss/login.png)

### Registration Page

![Home](ss/register.png)

### Dashboard

![Home](ss/dashboard.png)

### To-Do Page

![Home](ss/todo.png)

### Project Page

![Home](ss/project.png)

### Team Page

![Home](ss/task.png)

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to create a pull request.
