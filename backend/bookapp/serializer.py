from rest_framework import serializers
from .models import Librarian, Member, Book, Borrowing
from datetime import datetime, timedelta

class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = ['id', 'username', 'email', 'phone', 'is_active', 'is_admin', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class LibrarianCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = ['username', 'email', 'password', 'phone', 'is_admin']
        extra_kwargs = {'password': {'write_only': True}}

class MemberSerializer(serializers.ModelSerializer):
    membership_type_display = serializers.CharField(source='get_membership_type_display', read_only=True)
    
    class Meta:
        model = Member
        fields = ['id', 'username', 'email', 'phone', 'address', 'membership_number', 'membership_type', 'membership_type_display', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['username', 'email', 'password', 'phone', 'address', 'membership_type']
        extra_kwargs = {'password': {'write_only': True}}

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'ISBN', 'category', 'availability', 'image_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class BorrowingSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Borrowing
        fields = ['id', 'member', 'member_name', 'book', 'book_title', 'borrowed_date', 'due_date', 'returned_date', 'status', 'status_display']
        read_only_fields = ['id', 'borrowed_date', 'status_display']