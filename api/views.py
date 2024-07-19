from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()
# Create your views here.
"""                                     USER VIEWS                                                                      """
#user registration
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#User log in view
class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)
                
            response_data = {
                'message': 'User logged in successfully',
                'email': user.email,
                'token': token.key
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid email and/or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
#User list
class AllUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#User update password
class UserUpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        if not check_password(current_password, user.password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        if len(new_password) < 8:
            return Response({'error': 'New password must be at least 8 characters long'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
#Admin change employee role
class ChangeUserRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role not in ['admin', 'superadmin']:
            return Response(
                {'error': 'You are not authorized to change user roles.'},
                status=status.HTTP_403_FORBIDDEN
            )

        email = request.data.get('email')
        new_role = request.data.get('new_role')

        if not email or not new_role:
            return Response(
                {'error': 'Email and new role are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_role not in ['admin', 'employee', 'superadmin']:
            return Response(
                {'error': 'Invalid role specified.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        user.role = new_role
        user.save()

        return Response(
            {'success': f'User role updated to {new_role}.'},
            status=status.HTTP_200_OK
        )
#delete a user from the database
class DeleteUserView(APIView):
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        # Check if the current user has the admin or superadmin role
        if request.user.role not in ['admin', 'superadmin']:
            return Response(
                {'error': 'You are not authorized to delete users.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get the email from the request data
        email = request.data.get('email')

        # Check if email is provided
        if not email:
            return Response(
                {'error': 'Email is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to find the user with the provided email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the user
        user.delete()

        # Return a success response
        return Response(
            {'success': 'User deleted successfully.'},
            status=status.HTTP_200_OK
        )
    """                                     ASSET VIEWS                                                                     """
    #Add asset
class AssetAddView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        serializer = AssetSerializer(data=request.data)
        user=request.user
        if user.role=="employee":
            return Response(
                {'error': 'You are not authorized to add assets'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#get all assets
class AssetListView(APIView):
    def get(self, request):

        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)
#request for asset
class AssetUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, asset_id):
        user = request.user
        if user.role != 'employee':
            return Response(
                {'error': 'Only employees can request an asset.'},
                status=status.HTTP_403_FORBIDDEN
            )

        asset = get_object_or_404(Asset, id=asset_id)

        if not asset.status:
            return Response(
                {'error': 'Asset is already requested or not available.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Change the asset status to False (requested)
        asset.status = False
        asset.save()

        # Log the request in the Request table
        request_log = Request.objects.create(
            asset=asset,
            employee=user,
            status="pending"
        )

        return Response(
            {'success': 'Asset requested successfully and logged.'},
            status=status.HTTP_200_OK
        )
"""                                             REQUEST VIEWS"""
#request list
class RequestListView(APIView):
    def get(self, request):
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#request action(accept or deny)
class RequestActionView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, request_id):
        user = request.user
        if user.role not in ['admin', 'superadmin']:
            return Response(
                {'error': 'Only admins or superadmins can approve or reject requests.'},
                status=status.HTTP_403_FORBIDDEN
            )

        request_instance = get_object_or_404(Request, id=request_id)
        action = request.data.get('action')  # 'approve' or 'reject'

        if action == 'approve':
            request_instance.status = 'approved'
            request_instance.save()

            # Assuming you want to set asset status to False upon approval
            request_instance.asset.status = False
            request_instance.asset.save()

            return Response(
                {'success': 'Request approved successfully.'},
                status=status.HTTP_200_OK
            )

        elif action == 'reject':
            request_instance.status = 'rejected'
            request_instance.save()

            # Set asset status back to True upon rejection
            request_instance.asset.status =True
            request_instance.asset.save()

            return Response(
                {'success': 'Request rejected successfully.'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'Invalid action. Use "approve" or "reject".'},
            status=status.HTTP_400_BAD_REQUEST
        )