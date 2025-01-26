from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, MessageViewSet, ConversationViewSet
from drf_nested_routers import NestedDefaultRouter # type: ignore


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'conversations', ConversationViewSet)

conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

conversation_router.register(r'participants', UserViewSet, basename='conversation-participants')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]