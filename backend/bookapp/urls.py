from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('signup/', views.SignupView, name='signup'),
    path('login/', views.LoginView, name='login'),

    # User CRUD
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),

    # Book CRUD
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
