from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path,include
from api.views import GoogleLogin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('api.urls')),
    
    #Google login
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),
   
    # dj auth
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
