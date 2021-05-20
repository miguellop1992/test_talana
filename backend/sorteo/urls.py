from django.urls import path, include
from rest_framework import routers

from backend.sorteo.views import UserViewSet, LotteryViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'lottery', LotteryViewSet, basename='lottery')

urlpatterns = [
    path('', include(router.urls))
]
