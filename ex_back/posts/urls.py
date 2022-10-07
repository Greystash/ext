from django.urls import path

from .views import (
    ListCreatePostView,
    RetrieveDeletePostView,
    ListPostTagView
)


urlpatterns = [
    path('', ListCreatePostView.as_view()),
    path('<pk>', RetrieveDeletePostView.as_view()),
    path('tags/', ListPostTagView.as_view())
]
