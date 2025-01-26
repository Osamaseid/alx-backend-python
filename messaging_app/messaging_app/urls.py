
from django.contrib import admin
from django.urls import path, include
from chats.urls import main_api_urlpatterns, auth_api_urlpatterns
from rest_framework_simplejwt.views import TokenRefreshView
from chats.auth import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include(auth_api_urlpatterns)),
    path('api-auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(main_api_urlpatterns)),
]
