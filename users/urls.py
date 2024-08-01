from django.urls import path
from .views import SignupView, LoginView, SearchUserView,SendFriendRequestView,RespondFriendRequestView,ListPendingRequestsView,ListFriendsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchUserView.as_view(), name='search'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/respond/<int:request_id>/', RespondFriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('friend-request/pending/', ListPendingRequestsView.as_view(), name='pending-requests'),
]
