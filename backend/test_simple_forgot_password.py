#!/usr/bin/env python
"""
Test script for simplified forgot password functionality
Run this script to test the direct password reset functionality
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_forgot_password_flow():
    """Test the simplified forgot password flow"""
    
    print("=== Testing Simplified Forgot Password Functionality ===\n")
    
    # Get username and new password
    print("1. Enter credentials for password reset...")
    username = input("Enter username to reset password: ").strip()
    
    if not username:
        print("No username provided. Exiting.")
        return
    
    new_password = input("Enter new password (min 6 characters): ").strip()
    
    if len(new_password) < 6:
        print("❌ Password must be at least 6 characters long")
        return
    
    confirm_password = input("Confirm new password: ").strip()
    
    if new_password != confirm_password:
        print("❌ Passwords do not match")
        return
    
    try:
        response = requests.post(f"{BASE_URL}/forgot-password/", json={
            "username": username,
            "new_password": new_password
        })
        
        if response.status_code == 200:
            print("✅ Password reset successfully!")
            print("🎉 You can now login with your new password")
            print(f"📝 Response: {response.json()}")
        else:
            print(f"❌ Password reset failed: {response.json().get('error', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Django server is running on http://127.0.0.1:8000")
        return
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("Make sure your Django server is running on http://127.0.0.1:8000")
    print("You can start it with: python manage.py runserver\n")
    
    test_forgot_password_flow() 