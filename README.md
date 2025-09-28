# Healthcare Management System - Fullstack Application

A comprehensive fullstack healthcare management system built with Django, Django REST Framework, and PostgreSQL. Features both a modern web interface and RESTful API endpoints for secure patient and doctor management with JWT authentication.

## Features


### REST API
- **JWT Authentication**: Secure token-based authentication
- **Patient Management**: Full CRUD operations for patient records
- **Doctor Management**: Complete doctor profile management
- **Patient-Doctor Mapping**: Assign patients to doctors with status tracking
- **Secure Access**: Role-based permissions ensuring users can only access their own data
- **Admin Interface**: Django admin for easy data management
- **Error Handling**: Comprehensive error handling and validation
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Technology Stack

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript (ES6+)
- **Authentication**: JWT (djangorestframework-simplejwt 5.3.0)
- **Database**: PostgreSQL (with SQLite fallback for development)
- **Static Files**: Whitenoise for production static file serving
- **Environment Management**: python-decouple
- **CORS**: django-cors-headers

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Healthcare-backend-app
```

### 2. Create Virtual Environment
```bash
python3 -m venv healthcare_env
source healthcare_env/bin/activate  # On Windows: healthcare_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
The project uses a `.env` file for configuration. Default values are provided:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration (using SQLite for simplicity)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=healthcare_db.sqlite3

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
All endpoints (except registration and login) require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-access-token>
```

## API Endpoints

### 1. Authentication APIs

#### Register User
- **URL**: `POST /api/auth/register/`
- **Description**: Register a new user
- **Permissions**: Public
- **Request Body**:
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```
- **Response**:
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "tokens": {
        "refresh": "refresh-token",
        "access": "access-token"
    }
}
```

#### Login User
- **URL**: `POST /api/auth/login/`
- **Description**: Login existing user
- **Permissions**: Public
- **Request Body**:
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```
- **Response**:
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    },
    "tokens": {
        "refresh": "refresh-token",
        "access": "access-token"
    }
}
```

#### Get User Profile
- **URL**: `GET /api/auth/profile/`
- **Description**: Get current user profile
- **Permissions**: Authenticated users only

#### Refresh Token
- **URL**: `POST /api/auth/token/refresh/`
- **Description**: Refresh access token
- **Request Body**:
```json
{
    "refresh": "refresh-token"
}
```

### 2. Patient Management APIs

#### List/Create Patients
- **URL**: `GET/POST /api/patients/`
- **Description**: List all patients created by user or create new patient
- **Permissions**: Authenticated users only

**GET Response**:
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "first_name": "Jane",
            "last_name": "Smith",
            "full_name": "Jane Smith",
            "email": "jane@example.com",
            "phone_number": "+1234567890",
            "date_of_birth": "1990-01-15",
            "gender": "F",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "blood_type": "O+",
            "allergies": "None",
            "medical_history": "No significant medical history",
            "created_by_username": "johndoe",
            "created_at": "2023-01-01T12:00:00Z",
            "updated_at": "2023-01-01T12:00:00Z"
        }
    ]
}
```

**POST Request**:
```json
{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "phone_number": "+1234567890",
    "date_of_birth": "1990-01-15",
    "gender": "F",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "blood_type": "O+",
    "allergies": "None",
    "medical_history": "No significant medical history"
}
```

#### Patient Details
- **URL**: `GET/PUT/DELETE /api/patients/<id>/`
- **Description**: Get, update, or delete specific patient
- **Permissions**: Authenticated users (own patients only)

### 3. Doctor Management APIs

#### List Doctors
- **URL**: `GET /api/doctors/`
- **Description**: List all available doctors
- **Permissions**: Authenticated users only

#### Create Doctor
- **URL**: `POST /api/doctors/create/`
- **Description**: Create new doctor profile
- **Permissions**: Authenticated users only
- **Request Body**:
```json
{
    "first_name": "Dr. Sarah",
    "last_name": "Johnson",
    "email": "sarah.johnson@hospital.com",
    "phone_number": "+1987654321",
    "specialization": "CARDIOLOGY",
    "license_number": "MD123456",
    "years_of_experience": 10,
    "qualification": "MD, FACC",
    "clinic_name": "Heart Care Clinic",
    "clinic_address": "456 Medical Center Dr",
    "city": "Boston",
    "state": "MA",
    "zip_code": "02101",
    "consultation_fee": 200.00,
    "is_available": true
}
```

#### Doctor Details
- **URL**: `GET /api/doctors/<id>/`
- **Description**: Get doctor details
- **Permissions**: Authenticated users only

#### Update Doctor
- **URL**: `PUT/PATCH /api/doctors/<id>/update/`
- **Description**: Update doctor details (only by creator)
- **Permissions**: Authenticated users (own doctors only)

#### Delete Doctor
- **URL**: `DELETE /api/doctors/<id>/delete/`
- **Description**: Delete doctor profile (only by creator)
- **Permissions**: Authenticated users (own doctors only)

### 4. Patient-Doctor Mapping APIs

#### List/Create Mappings
- **URL**: `GET/POST /api/mappings/`
- **Description**: List all mappings or assign patient to doctor
- **Permissions**: Authenticated users only

**POST Request**:
```json
{
    "patient": 1,
    "doctor": 1,
    "status": "ACTIVE",
    "notes": "Regular checkup scheduled"
}
```

#### Get Patient's Doctors
- **URL**: `GET /api/mappings/patient/<patient_id>/`
- **Description**: Get all doctors assigned to specific patient
- **Permissions**: Authenticated users (own patients only)

#### Update Mapping
- **URL**: `PUT/PATCH /api/mappings/<id>/update/`
- **Description**: Update mapping status or notes
- **Permissions**: Authenticated users (own mappings only)

#### Delete Mapping
- **URL**: `DELETE /api/mappings/<id>/`
- **Description**: Remove doctor from patient
- **Permissions**: Authenticated users (own mappings only)

## Model Specifications

### Patient Model
- **Personal Info**: first_name, last_name, email, phone_number, date_of_birth, gender
- **Address**: address, city, state, zip_code
- **Medical**: blood_type, allergies, medical_history
- **System**: created_by, created_at, updated_at

### Doctor Model
- **Personal Info**: first_name, last_name, email, phone_number
- **Professional**: specialization, license_number, years_of_experience, qualification
- **Clinic**: clinic_name, clinic_address, city, state, zip_code
- **Business**: consultation_fee, is_available
- **System**: created_by, created_at, updated_at

### PatientDoctorMapping Model
- **Relationships**: patient, doctor, created_by
- **Details**: assigned_date, status, notes
- **System**: created_at, updated_at

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:

- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

Error responses follow this format:
```json
{
    "error": "Error type",
    "message": "Detailed error message",
    "status_code": 400
}
```

## Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **User Isolation**: Users can only access their own data
3. **Input Validation**: Comprehensive data validation
4. **CORS Configuration**: Secure cross-origin requests
5. **Environment Variables**: Sensitive data in environment files

## Web Interface

The application provides a modern, responsive web interface built with Bootstrap 5:

- **Home Page**: `http://localhost:8000/` - Landing page with feature overview
- **Authentication**: 
  - Register: `http://localhost:8000/register/`
  - Login: `http://localhost:8000/login/`
  - Profile: `http://localhost:8000/profile/`
- **Dashboard**: `http://localhost:8000/dashboard/` - Main dashboard with statistics
- **Patient Management**: `http://localhost:8000/patients/` - Patient records with search/filter
- **Doctor Directory**: `http://localhost:8000/doctors/` - Browse available doctors
- **Assignments**: `http://localhost:8000/assignments/` - Patient-doctor mappings
- **API Testing**: `http://localhost:8000/api-test/` - Built-in API testing interface

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/` with superuser credentials to manage:
- Users
- Patients
- Doctors
- Patient-Doctor Mappings

## Testing

Test the API using tools like Postman, curl, or any HTTP client. Example requests are provided in the API documentation above.

## Deployment Considerations

For production deployment:

1. Change `DEBUG = False` in settings
2. Use a production database (PostgreSQL recommended)
3. Set a strong `SECRET_KEY`
4. Configure proper `ALLOWED_HOSTS`
5. Use environment variables for all sensitive data
6. Set up proper logging
7. Use HTTPS
8. Configure static files serving

## Support

For questions or issues, please refer to the Django and Django REST Framework documentation:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## License

This project is for educational/development purposes. Please ensure compliance with healthcare data regulations (HIPAA, etc.) before using in production.
