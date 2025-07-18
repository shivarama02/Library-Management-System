#!/usr/bin/env python
"""
Script to create test data for the Library Management System
Run this script to quickly set up test users and books
"""

import os
import sys
import django
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from bookapp.models import User, Book
from django.contrib.auth.hashers import make_password

def create_test_data():
    print("🚀 Creating test data for Library Management System...")
    
    # Create test users
    users_data = [
        {
            'username': 'librarian1',
            'email': 'librarian1@library.com',
            'password': 'password123',
            'role': 'librarian'
        },
        {
            'username': 'librarian2',
            'email': 'librarian2@library.com',
            'password': 'password123',
            'role': 'librarian'
        },
        {
            'username': 'member1',
            'email': 'member1@library.com',
            'password': 'password123',
            'role': 'member'
        },
        {
            'username': 'member2',
            'email': 'member2@library.com',
            'password': 'password123',
            'role': 'member'
        },
        {
            'username': 'admin',
            'email': 'admin@library.com',
            'password': 'admin123',
            'role': 'librarian'
        }
    ]
    
    # Create users
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'password': make_password(user_data['password']),
                'role': user_data['role'],
                'is_active': True
            }
        )
        if created:
            print(f"✅ Created user: {user.username} ({user.get_role_display()})")
        else:
            print(f"ℹ️  User already exists: {user.username}")
    
    # Create test books
    books_data = [
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'ISBN': '9780743273565',
            'category': 'Fiction',
            'availability': True
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'ISBN': '9780446310789',
            'category': 'Fiction',
            'availability': True
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'ISBN': '9780451524935',
            'category': 'Fiction',
            'availability': True
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'ISBN': '9780141439518',
            'category': 'Literature',
            'availability': True
        },
        {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'ISBN': '9780547928241',
            'category': 'Fiction',
            'availability': True
        },
        {
            'title': 'Python Programming',
            'author': 'John Smith',
            'ISBN': '9781234567890',
            'category': 'Technology',
            'availability': True
        },
        {
            'title': 'Data Science Handbook',
            'author': 'Sarah Johnson',
            'ISBN': '9780987654321',
            'category': 'Science',
            'availability': True
        },
        {
            'title': 'World History',
            'author': 'Michael Brown',
            'ISBN': '9781122334455',
            'category': 'History',
            'availability': True
        }
    ]
    
    # Create books
    for book_data in books_data:
        book, created = Book.objects.get_or_create(
            ISBN=book_data['ISBN'],
            defaults=book_data
        )
        if created:
            print(f"✅ Created book: {book.title} by {book.author}")
        else:
            print(f"ℹ️  Book already exists: {book.title}")
    
    print("\n🎉 Test data creation completed!")
    print("\n📋 Login Credentials:")
    print("=" * 50)
    print("Librarian Accounts:")
    print("- Username: librarian1, Password: password123")
    print("- Username: librarian2, Password: password123")
    print("- Username: admin, Password: admin123")
    print("\nMember Accounts:")
    print("- Username: member1, Password: password123")
    print("- Username: member2, Password: password123")
    print("\n🌐 Access URLs:")
    print("- Frontend: http://localhost:3000")
    print("- Backend API: http://127.0.0.1:8000")
    print("- Admin Panel: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    create_test_data() 