# Healthcare Backend Deployment Guide

## Free Deployment Options

### Recommended: Railway.app
- Free PostgreSQL database included
- Easy deployment from GitHub
- Automatic HTTPS

### Alternative: Render.com
- Free PostgreSQL database
- GitHub integration
- Automatic deployments

## Environment Variables

Set these environment variables in your deployment platform:

### Required Variables
```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
```

### Database Variables (PostgreSQL)
```
DB_NAME=healthcare_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
```

### Optional Variables
```
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
ALLOWED_HOSTS=your-domain.railway.app,localhost,127.0.0.1
SECURE_SSL_REDIRECT=True
```

## Deployment Steps

### Railway.app Deployment

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Add PostgreSQL Database**
   - In your project dashboard, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically create connection variables

4. **Configure Environment Variables**
   - Go to your service settings
   - Add all the environment variables listed above
   - Railway will auto-populate database variables

5. **Deploy**
   - Railway will automatically deploy on every push to main branch
   - Check deployment logs for any issues

### Render.com Deployment

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create PostgreSQL Database**
   - Click "New" → "PostgreSQL"
   - Choose free tier
   - Note down the connection details

3. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn healthcare_backend.wsgi:application`

4. **Add Environment Variables**
   - In service settings, add all variables
   - Use the PostgreSQL connection details from step 2

## API Endpoints

Your deployed API will be available at:
- `https://your-app-name.railway.app/api/`
- `https://your-app-name.onrender.com/api/`

### Available Endpoints:
```
Authentication:
POST /api/auth/register/     - User registration
POST /api/auth/login/        - User login
POST /api/auth/logout/       - User logout
GET  /api/auth/profile/      - Get user profile
POST /api/auth/token/refresh/ - Refresh JWT token

Patients:
GET  /api/patients/          - List patients
POST /api/patients/          - Create patient
GET  /api/patients/<id>/     - Get patient details
PUT  /api/patients/<id>/     - Update patient
DELETE /api/patients/<id>/   - Delete patient

Doctors:
GET  /api/doctors/           - List doctors
POST /api/doctors/create/    - Create doctor
GET  /api/doctors/<id>/      - Get doctor details
PUT  /api/doctors/<id>/update/ - Update doctor
DELETE /api/doctors/<id>/delete/ - Delete doctor

Mappings:
GET  /api/mappings/          - List patient-doctor mappings
POST /api/mappings/          - Create mapping
PUT  /api/mappings/<id>/update/ - Update mapping
DELETE /api/mappings/<id>/   - Delete mapping
GET  /api/mappings/patient/<id>/ - Get patient's doctors
```

## Frontend Configuration

Update your frontend to use the deployed API URL:
```javascript
const API_BASE_URL = 'https://your-app-name.railway.app/api';
// or
const API_BASE_URL = 'https://your-app-name.onrender.com/api';
```

## Security Notes

- Never commit sensitive environment variables to Git
- Use strong, unique SECRET_KEY in production
- Enable HTTPS in production (automatic with Railway/Render)
- Monitor your application logs regularly

## Troubleshooting

### Common Issues:
1. **Database Connection Error**: Check DB credentials
2. **CORS Error**: Verify frontend domain in CORS_ALLOWED_ORIGINS
3. **Static Files**: Whitenoise handles static files automatically
4. **Migration Error**: Check database permissions

### Logs:
- Railway: View in dashboard logs tab
- Render: View in service logs section
