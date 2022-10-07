from django.urls import path
from rest_framework import routers

from .views import (GetUsersView, LoginView, LogoutView, RegisterView,
                    PatchView, UpdatePasswordView,
                    UpdateUserGroupsView)

router = routers.SimpleRouter()

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('update-user/', PatchView.as_view()),
    path('update-password/', UpdatePasswordView.as_view()),
    path('update-groups/', UpdateUserGroupsView.as_view()),
    path('get-users/', GetUsersView.as_view())
]