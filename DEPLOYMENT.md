# Healthcare Backend - Render Deployment Guide

## Prerequisites
- GitHub repository with your code
- Render account (free tier available)

## Step 1: Prepare Your Repository
1. Push all changes to your GitHub repository
2. Ensure all files are committed:
   - `render.yaml`
   - `build.sh`
   - `requirements.txt`
   - Updated `settings.py`

## Step 2: Create PostgreSQL Database on Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `healthcare-postgres`
   - **Database**: `healthcare_db`
   - **User**: `healthcare_user`
   - **Plan**: Free (or paid if needed)
4. Click "Create Database"
5. **Important**: Copy the "External Database URL" - you'll need this

## Step 3: Deploy Web Service on Render
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `healthcare-backend`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn healthcare_backend.wsgi:application`
   - **Plan**: Free (or paid if needed)

## Step 4: Set Environment Variables
In your web service settings, add these environment variables:

### Required Variables:
- `DATABASE_URL`: (Use the External Database URL from Step 2)
- `DEBUG`: `False`
- `SECRET_KEY`: Generate a secure secret key
- `ALLOWED_HOSTS`: `your-app-name.onrender.com`

### Optional Variables:
- `JWT_ACCESS_TOKEN_LIFETIME_MINUTES`: `60`
- `JWT_REFRESH_TOKEN_LIFETIME_DAYS`: `7`

## Step 5: Deploy
1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. Wait for deployment to complete (usually 5-10 minutes)

## Step 6: Test Your Deployment
Your API will be available at: `https://your-app-name.onrender.com/api/`

Test endpoints:
- `GET https://your-app-name.onrender.com/api/` - API root
- `POST https://your-app-name.onrender.com/api/auth/register/` - Register
- `POST https://your-app-name.onrender.com/api/auth/login/` - Login

## Configured Frontend Domains
Your backend is configured to accept requests from:
- `https://hospital-frontend-app.vercel.app`
- `https://hospital-frontend-app-parthkhandelwal0077s-projects.vercel.app`
- Local development: `http://localhost:3000`

## Important Notes
1. **Free Tier Limitations**: 
   - Service spins down after 15 minutes of inactivity
   - First request after spin-down may be slow (cold start)
   - PostgreSQL free tier has connection limits

2. **Database Migrations**: 
   - Migrations run automatically during deployment via `build.sh`
   - If you add new models, they'll be migrated on next deployment

3. **Static Files**: 
   - Handled by WhiteNoise (already configured)
   - No additional setup needed

4. **Monitoring**: 
   - Check Render dashboard for logs and metrics
   - Logs are available in the web service dashboard

## Troubleshooting
- **500 Errors**: Check environment variables, especially `DATABASE_URL`
- **CORS Issues**: Verify frontend domain is in `CORS_ALLOWED_ORIGINS`
- **Database Issues**: Ensure PostgreSQL service is running
- **Build Failures**: Check `build.sh` and `requirements.txt`

## Local Development vs Production
- **Local**: Uses SQLite database
- **Production**: Uses PostgreSQL (when `DATABASE_URL` is set)
- **Debug Mode**: Automatically disabled in production when `DEBUG=False`
