# users/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from users.models import Customer

from .serializers import UserRegistrationSerializer, UserSerializer , CustomerSerializer


@api_view(['POST'])
@permission_classes([AllowAny])  # Anyone can register
def register(request):
    """
    Register a new user
    POST /api/users/register/
    Body: {
        "username": "john",
        "email": "john@example.com",
        "password": "password123",
        "password2": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])  # Anyone can login
def create_customer(request):
    """
    Create a new customer profile (admin only)
    POST /api/users/create_customer/
    Body: {
        "user": 1,
        "role": "customer",
        "user_type": "individual",
        "phone": "1234567890",
        "address": "123 Main St",
        "company_name": "",
        "ice": ""
    }
    """
    serializer = CustomerSerializer(data=request.data)
    
    if serializer.is_valid():
        customer = serializer.save()
        return Response({
            'message': 'Customer profile created successfully',
            'customer': CustomerSerializer(customer).data
        }, 
        status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def list_customers(request):
    """
    List all customer profiles (admin only)
    GET /api/users/list_customers/
    """
    try:
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'An error occurred while fetching customers'
        }, 
    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])  # Anyone can login
def login(request):
    """
    Login user
    POST /api/users/login/
    Body: {
        "username": "john",
        "password": "password123"
    }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    return Response({
        'error': 'Invalid username or password'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Must be logged in
def profile(request):
    """
    Get current user profile (requires token)
    GET /api/users/profile/
    Headers: Authorization: Bearer <access_token>
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout user (blacklist refresh token)
    POST /api/users/logout/
    Body: {
        "refresh": "<refresh_token>"
    }
    """
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)