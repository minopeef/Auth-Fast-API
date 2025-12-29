# FastAPI Application Template with Authentication and Authorization

This project is a ready-to-use template for developing scalable web applications based on **FastAPI** with
a complete authentication and authorization system. The project includes a modular architecture, supports flexible
logging with **loguru**, and database interaction through **SQLAlchemy** with async support. The **Alembic**
migration system simplifies working with the database schema.

## Key Features

- ✅ **Authentication and Authorization** - Complete system for login, registration, and user management
- ✅ **JWT Tokens** - Secure authorization using access and refresh tokens
- ✅ **User Roles** - Support for regular users and administrators
- ✅ **Async Database Operations** - Using SQLAlchemy 2.0 with async support
- ✅ **Database Migrations** - Database schema management through Alembic
- ✅ **Data Validation** - Pydantic schemas for input and output data validation
- ✅ **Logging** - Integration with loguru for convenient logging
- ✅ **CORS Support** - Configured CORS middleware for frontend integration
- ✅ **Automatic Documentation** - Swagger UI and ReDoc out of the box
- ✅ **Modular Architecture** - Clear separation into modules for easy extension

## Technology Stack

- **Web Framework**: FastAPI
- **ORM**: SQLAlchemy with async support via aiosqlite
- **Database**: SQLite (easily replaceable with another SQL database)
- **Migration System**: Alembic
- **Authorization/Authentication**: bcrypt for password hashing, python-jose for data protection using JWT

## Project Dependencies

- `fastapi[all]==0.115.0` - High-performance web framework
- `pydantic==2.9.2` - Data validation
- `pydantic[email]` - Email address validation support
- `pydantic_settings==2.5.2` - Environment variable settings management
- `uvicorn==0.31.0` - ASGI server
- `jinja2==3.1.4` - Template engine
- `SQLAlchemy==2.0.35` - ORM for database operations
- `aiosqlite==0.20.0` - Async support for SQLite
- `alembic==1.13.3` - Database migration management
- `bcrypt==4.0.1` and `passlib[bcrypt]==1.7.4` - Password hashing
- `python-jose==3.3.0` - JWT token operations
- `loguru==0.7.2` - Beautiful and convenient logging

## Project Structure

The project is built with a modular architecture in mind, which allows easy application extension and simplifies maintenance.
Each module is responsible for separate tasks, such as authorization or data management.

### Main Project Structure

```
├── app/
│   ├── auth/                   # Authentication and authorization module
│   │   ├── dao.py              # Data Access Object for database operations
│   │   ├── models.py           # Data models for authorization
│   │   ├── router.py           # FastAPI routers for routing
│   │   ├── schemas.py          # Schemas for data validation
│   │   └── utils.py            # Helper functions for authorization
│   ├── dao/                    # Common DAO for the application
│   │   ├── database.py         # Database connection and session management
│   │   └── base.py             # Base DAO class for database operations
│   ├── dependencies            # Project dependencies
│   │   ├── auth_dep.py         # Dependencies for authorization
│   │   └── dao_dep.py          # Dependencies for SQLAlchemy sessions
│   ├── migration/              # Database migrations
│   │   ├── versions/           # Migration files
│   │   ├── env.py              # Environment settings for Alembic
│   │   ├── README              # Migration documentation
│   │   └── script.py.mako      # Template for generating migrations
│   ├── static/                 # Application static files
│   │   └── .gitkeep            # Empty file to keep folder in Git
│   ├── config.py               # Application configuration
│   ├── exceptions.py           # Exception handling
│   ├── main.py                 # Main file for running the application
├── data/                       # Folder for database file storage
│   └── db.sqlite3              # SQLite database file
├── .env                        # Environment configuration
├── alembic.ini                 # Alembic configuration
├── README.md                   # Project documentation
└── requirements.txt            # Project dependencies
```

### Main Modules

#### **app/auth** - Authentication and Authorization Module

The module is responsible for managing authentication (user login) and authorization (access verification) processes.  
Main files:

- **`dao.py`**: Data access object for users. Contains methods for database operations (create, update,
  search users, etc.).
- **`models.py`**: Defines ORM data models for users (e.g., Users table in the database).
- **`router.py`**: Router for routing requests related to authentication. Defines endpoints for login,
  registration, and access verification.
- **`schemas.py`**: Defines Pydantic schemas for input data validation and response structures (e.g., data format
  for user registration).
- **`utils.py`**: Helper functions for working with tokens (create, verify JWT) and password encryption.

---

#### **app/dao** - Base Data Access Layer

The module contains abstractions for database operations. Used for managing connections and implementing
CRUD operations.

- **`base.py`**: Base DAO class providing common methods for database operations, such as add,
  update, delete, and search records.
- **`database.py`**: Responsible for database connection, SQLAlchemy session management, and creating
  async connections (e.g., via `aiosqlite`).

---

#### **app/migration** - Database Migration Management with Alembic

The module simplifies database schema management and allows safe changes.

- **`versions/`**: Stores migration files automatically created by Alembic.
- **`env.py`**: Main configuration file for Alembic. Defines database connection and ORM interaction.
- **`script.py.mako`**: Template for generating new migration files.

---

#### **app/dependencies** - Project Dependencies

The module contains dependencies used in the project.

- **`auth_dep.py`**: Dependencies related to user authorization in the system
- **`dao_dep.py`**: Dependencies related to SQLAlchemy session management and working with BaseDao child classes

---

#### **config.py** - Application Settings and Configuration

- Defines application parameters loaded from the `.env` file. For example:
    - `SECRET_KEY`: Secret key for signing JWT.
    - `ALGORITHM`: Token hashing algorithm.
    - `DATABASE_URL`: URL for database connection.
- Provides convenient configuration management for different environments (local, test, production).

---

#### **main.py** - Main Application File

- **Application Initialization**: Configures the FastAPI application, including parameters such as name, version, and
  description.
- **Router Registration**: Registers routes defined in application modules, for example:
    - `app.auth.router` for authorization routes.
    - Any additional modules (e.g., `app.users.router`).
- **Dependency Configuration**: Injects global dependencies, such as database connection or configuration
  parameters.
- **Middleware Configuration**: Adds intermediate layers for request processing (e.g., CORS, compression, error
  handling).
- **Error Handling**: Defines global exception handlers to return clear responses when errors occur
  (e.g., 401 Unauthorized or 500 Internal Server Error).
- **Server Startup**: Used to start the application using an ASGI server (Uvicorn).

## API Endpoints

### Authentication and Authorization (`/auth`)

- **POST `/auth/register/`** - Register a new user
  - Accepts: email, password, confirm_password
  - Returns: success message

- **POST `/auth/login/`** - Login to the system
  - Accepts: email, password
  - Sets cookies with access and refresh tokens
  - Returns: success message

- **POST `/auth/logout`** - Logout from the system
  - Removes tokens from cookies
  - Returns: success message

- **GET `/auth/me/`** - Get current user information
  - Requires: authorization (access token)
  - Returns: user information

- **GET `/auth/all_users/`** - Get list of all users
  - Requires: authorization with admin privileges
  - Returns: list of all users

- **POST `/auth/refresh`** - Refresh access tokens
  - Requires: refresh token in cookie
  - Sets new access and refresh tokens
  - Returns: success message

### Root Endpoint

- **GET `/`** - Home page
  - Returns: welcome message and project information

## Authentication and Authorization Setup

Authentication uses JSON Web Token (JWT) with bcrypt for password hashing and python-jose for token generation and
verification. This ensures secure data storage and protects API endpoints.

Tokens are stored in HTTP-only cookies for enhanced security. The system supports:
- Access tokens for accessing protected endpoints
- Refresh tokens for refreshing access tokens
- User roles (regular user and administrator)

## Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/Yakvenalex/FastApiWithAuthSample.git .
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create and configure `.env` file in the project root:

   ```env
   SECRET_KEY=your-super-secret-key-here-change-in-production
   ALGORITHM=HS256
   ```

   **Important**: 
   - `SECRET_KEY` should be long and random for security (minimum 32 characters recommended)
   - `ALGORITHM` defines the JWT token signing algorithm (usually HS256)
   - SQLite database will be automatically created in the `data/` folder on first migration run

4. Apply database migrations (if not already applied):

   ```bash
   alembic upgrade head
   ```

5. Run the application with Uvicorn:

   ```bash
   uvicorn app.main:app --reload --port 8005
   ```

   Replace the port if necessary.

6. After startup, the application will be available at:
   - **API**: http://localhost:8005
   - **Interactive Documentation (Swagger UI)**: http://localhost:8005/docs
   - **Alternative Documentation (ReDoc)**: http://localhost:8005/redoc

## Database Migrations

The project is already configured with Alembic for database migration management.

### Applying Existing Migrations

```bash
alembic upgrade head
```

### Creating a New Migration

After changing models in `app/auth/models.py` or other modules:

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Rolling Back Migrations

```bash
# Rollback one migration
alembic downgrade -1

# Rollback all migrations
alembic downgrade base
```

### Viewing Migration History

```bash
alembic history
```

### Viewing Current Version

```bash
alembic current
```

## API Testing

After starting the application, you can test the API in several ways:

### 1. Through Interactive Swagger UI Documentation

Open in browser: http://localhost:8005/docs

Here you can:
- View all available endpoints
- Test the API directly in the browser
- See request and response schemas

### 2. Through ReDoc

Open in browser: http://localhost:8005/redoc

Alternative documentation with a more readable format.

### 3. Through curl or Postman

Example user registration:
```bash
curl -X POST "http://localhost:8005/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "confirm_password": "securepassword123"
  }'
```

Example login:
```bash
curl -X POST "http://localhost:8005/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }' \
  -c cookies.txt
```

Example getting current user information:
```bash
curl -X GET "http://localhost:8005/auth/me/" \
  -b cookies.txt
```

## Environment Variables

The project uses the following environment variables (stored in `.env` file):

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Secret key for signing JWT tokens | Yes | `your-super-secret-key-here` |
| `ALGORITHM` | JWT signing algorithm | Yes | `HS256` |

SQLite database is automatically created in the `data/db.sqlite3` folder on first migration run.

## Best Practices

- Separate application functionality into modules for easier testing and maintenance.
- Handle errors with clear responses and HTTP codes.
- Use Alembic migrations for database schema management.
- Use environment variables for secure storage of sensitive data.
- Regularly update dependencies to get security fixes.
- Use strong passwords and long secret keys in production environment.

## Development

### Adding New Modules

1. Create a new folder in `app/` with your module
2. Create necessary files: `models.py`, `schemas.py`, `dao.py`, `router.py`
3. Register the router in `app/main.py` in the `register_routers()` function

### Extending Functionality

The project is designed with extensibility in mind:
- Add new models to corresponding modules
- Create migrations for new database schema changes
- Use existing DAO classes as a basis for new ones

---

This template is a powerful and convenient foundation for developing FastAPI applications with authentication,
authorization, and structured architecture ready for scaling.

## Author

**Yakovenko Alexey**  
Telegram: [@PythonPathMaster](https://t.me/PythonPathMaster)  
Community: [Easy Path to Python](https://t.me/PythonPathMaster)
