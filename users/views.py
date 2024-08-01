from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FriendRequest, CustomUser
from .serializers import FriendRequestSerializer
from .serializers import UserSerializer, SignupSerializer

class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class SearchUserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '').lower()
        if '@' in keyword:
            return CustomUser.objects.filter(email__iexact=keyword)
        else:
            return CustomUser.objects.filter(username__icontains=keyword)



class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        to_user_email = request.data.get('email')
        try:
            to_user = CustomUser.objects.get(email=to_user_email)
            if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
                return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
            FriendRequest.objects.create(from_user=request.user, to_user=to_user, status='pending')
            return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class RespondFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, request_id):
        action = request.data.get('action')
        friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
        
        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({'message': 'Friend request rejected'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

class ListFriendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friends = CustomUser.objects.filter(sent_requests__to_user=request.user, sent_requests__status='accepted') | CustomUser.objects.filter(received_requests__from_user=request.user, received_requests__status='accepted')
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListPendingRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# users/views.py

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FriendRequest, CustomUser
from .serializers import FriendRequestSerializer, UserSerializer
from .throttling import FriendRequestThrottle

class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request):
        to_user_email = request.data.get('email')
        try:
            to_user = CustomUser.objects.get(email=to_user_email)
            if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
                return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
            FriendRequest.objects.create(from_user=request.user, to_user=to_user, status='pending')
            return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class RespondFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, request_id):
        action = request.data.get('action')
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
            if action == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()
                return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)
            elif action == 'reject':
                friend_request.status = 'rejected'
                friend_request.save()
                return Response({'message': 'Friend request rejected'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

class ListFriendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        friends = CustomUser.objects.filter(
            sent_requests__to_user=request.user, sent_requests__status='accepted'
        ) | CustomUser.objects.filter(
            received_requests__from_user=request.user, received_requests__status='accepted'
        )
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListPendingRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# views.py
import logging

logger = logging.getLogger(__name__)

class ListPendingRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        logger.info(f"Pending requests for {request.user.email}: {pending_requests.count()}")
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
