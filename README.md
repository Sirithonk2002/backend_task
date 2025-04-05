# Task Manager Backend API

This is the backend API for the Task Manager application, developed using **FastAPI** and **SQLAlchemy**. It provides functionality to manage tasks, including creating, updating, deleting, and organizing tasks by their status (To Do, In Progress, Done).

## Use Render for backend deployment
    https://backend-task-6pav.onrender.com

## Requirements

- Python 3.7+
- PostgreSQL 
- FastAPI
- SQLAlchemy
- Uvicorn (for running the application)
- CORS middleware for cross-origin requests

```bash
git clone https://github.com/Sirithonk2002/backend_task.git
```
2. Create a virtual environment
```bash
    python -m venv venv
    venv\Scripts\activate
```

3. Install dependencies
```bash
    pip install -r requirements.txt
```

4. Set Up the Database
```bash
    pip install -r requirements.txt
```

5. Set up the database
6. ```bash
DATABASE_URL=postgresql://task_admin:hYqIK8bRgevqPyf7VRZ2KD77ddjRck9t@dpg-cvn7e42dbo4c73bftkr0-a.oregon-postgres.render.com/task_app_kpou
```

7. Install python-dotenv
```bash
    pip install python-dotenv
```
7. Alembic
```bash
    pip install alembic
```

7. Run the application
```bash
    uvicorn app.main:app --reload
```

8. Testing the API
- POST /users/register (Register a new user.)
- POST /users/login (Log in and get an access token.)
- GET /tasks  (Retrieve tasks.)
- POST /tasks  (Create a new task.)
- PUT /tasks/{id}  (Update a task's details or status.)
- DELETE /tasks/{id}  (Delete a task.)
