#!/usr/bin/env python3
"""
Simple test script to verify the Healthcare Backend API endpoints
"""
import requests
import json
import time

BASE_URL = 'http://localhost:8000/api'

def test_api_root():
    """Test the API root endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/')
        print(f"✅ API Root: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"❌ API Root failed: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=user_data)
        print(f"✅ User Registration: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"User created: {data['user']['username']}")
            return data['tokens']['access']
        else:
            print(f"Registration response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ User Registration failed: {e}")
        return None

def test_user_login():
    """Test user login"""
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
        print(f"✅ User Login: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"User logged in: {data['user']['username']}")
            return data['tokens']['access']
        else:
            print(f"Login response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ User Login failed: {e}")
        return None

def test_protected_endpoint(token):
    """Test a protected endpoint with JWT token"""
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(f'{BASE_URL}/auth/profile/', headers=headers)
        print(f"✅ Protected Endpoint (Profile): {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Profile data: {data['user']['username']}")
            return True
        else:
            print(f"Profile response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Protected Endpoint failed: {e}")
        return False

def main():
    print("🏥 Healthcare Backend API Test")
    print("=" * 40)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test API root
    if not test_api_root():
        print("❌ Server might not be running. Please start with: python manage.py runserver")
        return
    
    print("\n" + "=" * 40)
    
    # Test registration
    access_token = test_user_registration()
    
    if not access_token:
        # If registration fails, try login (user might already exist)
        print("Registration failed, trying login...")
        access_token = test_user_login()
    
    if access_token:
        print("\n" + "=" * 40)
        # Test protected endpoint
        test_protected_endpoint(access_token)
        
        print("\n🎉 Basic API tests completed successfully!")
        print("\n📚 You can now test other endpoints using tools like Postman or curl")
        print("📖 Check the README.md for complete API documentation")
    else:
        print("❌ Authentication tests failed")

if __name__ == '__main__':
    main()
