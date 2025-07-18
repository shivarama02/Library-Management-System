# BookHub - Library Management System

A full-stack library management system built with Django REST API backend and React frontend.

## Features

- User authentication (signup/login)
- Book management (CRUD operations)
- User management
- Responsive Bootstrap UI
- Secure password hashing
- Input validation

## Project Structure

```
BOOKHUB/
├── backend/                 # Django REST API
│   ├── bookapp/            # Main Django app
│   ├── bookstore/          # Django project settings
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables (create this)
│   └── manage.py          # Django management script
└── frontend/              # React frontend
    └── bookapp/           # React application
        ├── src/
        │   ├── component/ # React components
        │   ├── App.js     # Main app component
        │   └── index.js   # Entry point
        └── package.json   # Node.js dependencies
```

## Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv env
   env\Scripts\activate
   
   # macOS/Linux
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Rename `env_file.txt` to `.env`
   - Update the database credentials in `.env` file:
     ```
     DB_NAME=your_database_name
     DB_USER=your_mysql_username
     DB_PASSWORD=your_mysql_password
     ```

5. **Set up MySQL database:**
   - Create a MySQL database named `library` (or update the name in `.env`)
   - Make sure MySQL server is running

6. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the Django server:**
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://127.0.0.1:8000/`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend/bookapp
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000/`

## API Endpoints

### Authentication
- `POST /signup/` - User registration
- `POST /login/` - User login

### Users
- `GET /users/` - List all users
- `POST /users/` - Create new user
- `GET /users/{id}/` - Get user details
- `PUT /users/{id}/` - Update user
- `DELETE /users/{id}/` - Delete user

### Books
- `GET /books/` - List all books
- `POST /books/` - Create new book
- `GET /books/{id}/` - Get book details
- `PUT /books/{id}/` - Update book
- `DELETE /books/{id}/` - Delete book

## Security Features

- ✅ Password hashing using Django's built-in hashers
- ✅ Input validation on both frontend and backend
- ✅ Environment variables for sensitive data
- ✅ CORS configuration for frontend-backend communication
- ✅ Proper error handling

## Technologies Used

### Backend
- Django 5.2.0
- Django REST Framework 3.14.0
- MySQL Database
- Python 3.x

### Frontend
- React 19.1.0
- React Router DOM 7.5.2
- Axios 1.9.0
- Bootstrap 5.3.5

## Troubleshooting

### Common Issues

1. **Database Connection Error:**
   - Ensure MySQL server is running
   - Check database credentials in `.env` file
   - Verify database exists

2. **CORS Error:**
   - Check CORS settings in `settings.py`
   - Ensure frontend URL is in `CORS_ALLOWED_ORIGINS`

3. **Module Not Found Error:**
   - Activate virtual environment
   - Install requirements: `pip install -r requirements.txt`

4. **Port Already in Use:**
   - Change port: `python manage.py runserver 8001`
   - Or kill the process using the port

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License. 