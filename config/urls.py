from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #  SWAGGER & API DOCUMENTATION
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API URLS
    path('api/v1/', include('api.urls')),
    
    #  WEB URLS
    path('', include('users.urls')),
    path('branches/', include('branches.urls')),
    path('subjects/', include('subjects.urls')),
    path('students/', include('students.urls')),
    path('groups/', include('groups.urls')),
    path('lessons/', include('lessons.urls')),
    path('attendance/', include('attendance.urls')),
]