from django.urls import path, include
from rest_framework import routers
from users.urls import router as users_router
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.registry.extend(users_router.registry)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('users.urls')),
    path('api/posts/', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
