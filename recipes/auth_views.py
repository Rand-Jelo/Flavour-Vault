from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# User Profile View (Retrieve and Update User Info)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Allows authenticated users to retrieve or update their profile."""
    user = request.user

    if request.method == 'GET':
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        })

    elif request.method == 'PUT':
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        
        if 'password' in request.data:
            user.set_password(request.data['password'])

        user.save()
        return Response({'message': 'Profile updated successfully'})

# Delete User Account
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """Allows authenticated users to delete their own account."""
    user = request.user
    user.delete()
    return Response({'message': 'User account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)