# users/throttling.py

from rest_framework.throttling import UserRateThrottle

class FriendRequestThrottle(UserRateThrottle):
    rate = '3/min'
