from django.contrib import admin
from .models import Librarian, Member, Book, Borrowing

# Customize admin site
admin.site.site_header = "BookHub Administration"
admin.site.site_title = "BookHub Admin Portal"
admin.site.index_title = "Welcome to BookHub Administration"

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_active', 'is_admin', 'created_at')
    list_filter = ('is_active', 'is_admin', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Information', {
            'fields': ('phone',)
        }),
        ('Status & Privileges', {
            'fields': ('is_active', 'is_admin')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'membership_type', 'is_active', 'created_at')
    list_filter = ('membership_type', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'membership_number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Information', {
            'fields': ('phone', 'address')
        }),
        ('Membership Information', {
            'fields': ('membership_number', 'membership_type')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'ISBN', 'category', 'availability', 'created_at')
    list_filter = ('category', 'availability', 'created_at')
    search_fields = ('title', 'author', 'ISBN', 'category')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'ISBN', 'category')
        }),
        ('Status', {
            'fields': ('availability',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('member', 'book', 'borrowed_date', 'due_date', 'returned_date', 'status')
    list_filter = ('status', 'borrowed_date', 'due_date', 'returned_date')
    search_fields = ('member__username', 'book__title', 'book__author')
    ordering = ('-borrowed_date',)
    readonly_fields = ('borrowed_date',)
    
    fieldsets = (
        ('Borrowing Information', {
            'fields': ('member', 'book', 'status')
        }),
        ('Dates', {
            'fields': ('borrowed_date', 'due_date', 'returned_date')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('member', 'book')
