#!/usr/bin/env python3
"""Test script for admin login endpoint"""

import requests
import json

# Test admin login
url = "http://localhost:8000/api/admin/login"
data = {
    "username": "admin",
    "password": "admin123"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✅ Login successful!")
        token = response.json().get("token")
        print(f"Token received: {token[:50]}...")
    else:
        print("\n❌ Login failed!")
        print(f"Error: {response.json()}")
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to server. Make sure backend is running at http://localhost:8000")
except Exception as e:
    print(f"❌ Error: {e}")


