from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('signup/', views.SignupView, name='signup'),
    path('login/', views.LoginView, name='login'),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),

    # Librarian CRUD
    path('librarians/', views.LibrarianListCreateView.as_view(), name='librarian-list-create'),
    path('librarians/<int:pk>/', views.LibrarianRetrieveUpdateDestroyView.as_view(), name='librarian-detail'),
    path('librarians/<int:pk>/password/', views.UpdateLibrarianPassword, name='librarian-password'),

    # Member CRUD
    path('members/', views.MemberListCreateView.as_view(), name='member-list-create'),
    path('members/<int:pk>/', views.MemberRetrieveUpdateDestroyView.as_view(), name='member-detail'),
    path('members/<int:pk>/password/', views.UpdateMemberPassword, name='member-password'),

    # Book CRUD
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),

    # Borrowing CRUD
    path('borrowings/', views.BorrowingListCreateView.as_view(), name='borrowing-list-create'),
    path('borrowings/<int:pk>/', views.BorrowingRetrieveUpdateDestroyView.as_view(), name='borrowing-detail'),

    # Member Borrowing Report
    path('members/<int:member_id>/report/', views.MemberBorrowingReportView, name='member-borrowing-report'),

    # Dashboard
    path('dashboard/stats/', views.DashboardStats, name='dashboard-stats'),
]
