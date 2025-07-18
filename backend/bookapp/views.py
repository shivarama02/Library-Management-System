from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from datetime import timedelta
from .models import Librarian, Member, Book, Borrowing
from .serializer import LibrarianSerializer, LibrarianCreateSerializer, MemberSerializer, MemberCreateSerializer, BookSerializer, BorrowingSerializer

# Authentication Views
@api_view(['POST'])
def SignupView(request):
    try:
        username = request.data.get('username', '').strip()
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '')
        user_type = request.data.get('user_type', 'member')  # 'librarian' or 'member'

        # Validation
        if not username or not email or not password:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(username) < 3:
            return Response({'error': 'Username must be at least 3 characters long'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(password) < 6:
            return Response({'error': 'Password must be at least 6 characters long'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists in either model
        if Librarian.objects.filter(username=username).exists() or Member.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Librarian.objects.filter(email=email).exists() or Member.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user based on type
        if user_type == 'librarian':
            user = Librarian.objects.create(
                username=username, 
                email=email, 
                password=password,
                phone=request.data.get('phone', ''),
                is_admin=request.data.get('is_admin', False)
            )
        else:
            import uuid
            membership_number = str(uuid.uuid4())[:8]
            user = Member.objects.create(
                username=username, 
                email=email, 
                password=password,
                phone=request.data.get('phone', ''),
                address=request.data.get('address', ''),
                membership_type=request.data.get('membership_type', 'regular'),
                membership_number=membership_number
            )
        
        return Response({'message': f'{user_type.title()} created successfully'}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': 'An error occurred during registration'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def LoginView(request):
    try:
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        # Validation
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Try to find user in both models
        librarian = Librarian.objects.filter(username=username).first()
        member = Member.objects.filter(username=username).first()
        
        user = None
        user_type = None
        
        if librarian and librarian.check_password(password):
            user = librarian
            user_type = 'librarian'
        elif member and member.check_password(password):
            user = member
            user_type = 'member'
        
        if user:
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user_type,
                    'is_active': user.is_active
                }
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    except Exception as e:
        return Response({'error': 'An error occurred during login'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Simple Forgot Password - Direct Password Reset
@api_view(['POST'])
def ForgotPassword(request):
    try:
        username = request.data.get('username', '').strip()
        new_password = request.data.get('new_password', '').strip()
        
        if not username or not new_password:
            return Response({'error': 'Username and new password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 6:
            return Response({'error': 'Password must be at least 6 characters long'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists in either model
        librarian = Librarian.objects.filter(username=username).first()
        member = Member.objects.filter(username=username).first()
        
        if not librarian and not member:
            return Response({'error': 'No account found with this username'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update password based on user type
        if librarian:
            librarian.set_password(new_password)
            user_type = 'librarian'
        else:
            member.set_password(new_password)
            user_type = 'member'
        
        return Response({
            'message': f'Password updated successfully for {user_type}',
            'user_type': user_type
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': 'An error occurred while resetting password'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Librarian CRUD
class LibrarianListCreateView(generics.ListCreateAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer

class LibrarianRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer

@api_view(['PUT'])
def UpdateLibrarianPassword(request, pk):
    try:
        librarian = Librarian.objects.get(pk=pk)
        new_password = request.data.get('password', '')
        
        if len(new_password) < 6:
            return Response({'error': 'Password must be at least 6 characters long'}, status=status.HTTP_400_BAD_REQUEST)
        
        librarian.set_password(new_password)
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
    
    except Librarian.DoesNotExist:
        return Response({'error': 'Librarian not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Member CRUD
class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def perform_create(self, serializer):
        import uuid
        membership_number = str(uuid.uuid4())[:8]
        serializer.save(membership_number=membership_number)

class MemberRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

@api_view(['PUT'])
def UpdateMemberPassword(request, pk):
    try:
        member = Member.objects.get(pk=pk)
        new_password = request.data.get('password', '')
        
        if len(new_password) < 6:
            return Response({'error': 'Password must be at least 6 characters long'}, status=status.HTTP_400_BAD_REQUEST)
        
        member.set_password(new_password)
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
    
    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Book CRUD
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            title = request.data.get('title', '').strip()
            author = request.data.get('author', '').strip()
            ISBN = request.data.get('ISBN', '').strip()
            category = request.data.get('category', '').strip()
            
            # Validation
            if not title or not author or not ISBN or not category:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(title) < 2:
                return Response({'error': 'Title must be at least 2 characters long'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(author) < 2:
                return Response({'error': 'Author must be at least 2 characters long'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(ISBN) < 10:
                return Response({'error': 'ISBN must be at least 10 characters long'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if ISBN already exists
            if Book.objects.filter(ISBN=ISBN).exists():
                return Response({'error': 'ISBN already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            return super().create(request, *args, **kwargs)
            
        except Exception as e:
            return Response({'error': 'An error occurred while creating the book'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def update(self, request, *args, **kwargs):
        try:
            title = request.data.get('title', '').strip()
            author = request.data.get('author', '').strip()
            ISBN = request.data.get('ISBN', '').strip()
            category = request.data.get('category', '').strip()
            
            # Validation
            if not title or not author or not ISBN or not category:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(title) < 2:
                return Response({'error': 'Title must be at least 2 characters long'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(author) < 2:
                return Response({'error': 'Author must be at least 2 characters long'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(ISBN) < 10:
                return Response({'error': 'ISBN must be at least 10 characters long'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if ISBN already exists (excluding current book)
            book = self.get_object()
            if Book.objects.filter(ISBN=ISBN).exclude(pk=book.pk).exists():
                return Response({'error': 'ISBN already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            return super().update(request, *args, **kwargs)
            
        except Exception as e:
            return Response({'error': 'An error occurred while updating the book'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Borrowing CRUD
class BorrowingListCreateView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            member_id = request.data.get('member')
            book_id = request.data.get('book')
            # due_date = request.data.get('due_date')  # Ignore this

            # Validation
            if not member_id or not book_id:
                return Response({'error': 'Member and book are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if member exists
            try:
                member = Member.objects.get(pk=member_id)
            except Member.DoesNotExist:
                return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

            # Check if book exists and is available
            try:
                book = Book.objects.get(pk=book_id)
                if not book.availability:
                    return Response({'error': 'Book is not available for borrowing'}, status=status.HTTP_400_BAD_REQUEST)
            except Book.DoesNotExist:
                return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

            # Set due_date to 10 days from now
            from django.utils import timezone
            from datetime import timedelta
            due_date = timezone.now() + timedelta(days=10)

            # Create borrowing
            borrowing = Borrowing.objects.create(
                member=member,
                book=book,
                due_date=due_date,
                status='borrowed'
            )

            # Update book availability
            book.availability = False
            book.save()

            return Response({
                'message': 'Book borrowed successfully',
                'borrowing': BorrowingSerializer(borrowing).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': 'An error occurred while creating the borrowing'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BorrowingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    
    def update(self, request, *args, **kwargs):
        try:
            borrowing = self.get_object()
            new_status = request.data.get('status')
            
            if new_status == 'returned' and borrowing.status != 'returned':
                # Update book availability
                book = borrowing.book
                book.availability = True
                book.save()
                
                # Update borrowing
                borrowing.status = 'returned'
                borrowing.returned_date = timezone.now()
                borrowing.save()
                
                return Response({
                    'message': 'Book returned successfully',
                    'borrowing': BorrowingSerializer(borrowing).data
                }, status=status.HTTP_200_OK)
            
            return super().update(request, *args, **kwargs)
            
        except Exception as e:
            return Response({'error': 'An error occurred while updating the borrowing'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def DashboardStats(request):
    try:
        total_books = Book.objects.count()
        total_members = Member.objects.count()
        total_librarians = Librarian.objects.count()
        total_borrowings = Borrowing.objects.count()
        active_borrowings = Borrowing.objects.filter(status='borrowed').count()
        overdue_borrowings = Borrowing.objects.filter(status='overdue').count()
        
        return Response({
            'total_books': total_books,
            'total_members': total_members,
            'total_librarians': total_librarians,
            'total_borrowings': total_borrowings,
            'active_borrowings': active_borrowings,
            'overdue_borrowings': overdue_borrowings,
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': 'An error occurred while fetching dashboard stats'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET'])
def MemberBorrowingReportView(request, member_id):
    try:
        member = Member.objects.get(pk=member_id)
        borrowings = Borrowing.objects.filter(member=member).order_by('-borrowed_date')
        data = BorrowingSerializer(borrowings, many=True).data
        return Response({'member': member.username, 'borrowings': data}, status=status.HTTP_200_OK)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'An error occurred while generating the report'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 