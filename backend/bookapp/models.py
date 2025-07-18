from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Librarian(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Increased for hashed passwords
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)  # For super admin privileges
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash password on creation
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def set_password(self, raw_password):
        """Set password with proper hashing"""
        self.password = make_password(raw_password)
        self.save(update_fields=['password'])

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"Librarian: {self.username}"

    class Meta:
        verbose_name = "Librarian"
        verbose_name_plural = "Librarians"
        ordering = ['-created_at']


class Member(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Increased for hashed passwords
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    membership_number = models.CharField(max_length=50, unique=True, blank=True)
    membership_type = models.CharField(max_length=20, choices=[
        ('student', 'Student'),
        ('regular', 'Regular'),
        ('premium', 'Premium'),
    ], default='regular')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash password on creation
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def set_password(self, raw_password):
        """Set password with proper hashing"""
        self.password = make_password(raw_password)
        self.save(update_fields=['password'])

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"Member: {self.username}"

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        ordering = ['-created_at']


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Borrowing(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    
    # Use Member model instead of User (nullable for migration)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrowings', null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed')
    
    def __str__(self):
        if self.member:
            return f"{self.member.username} borrowed {self.book.title}"
        return f"Unknown member borrowed {self.book.title}"
    
    class Meta:
        ordering = ['-borrowed_date']
