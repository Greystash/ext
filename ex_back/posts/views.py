from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Post, PostTag
from .serializers import PostSerializer, PostTagSerializer
from .filters import PostFilterSet
from .paginations import PostPagination
from users.permissions import IsStaffOrReadOnlyPermission


class ListCreatePostView(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsStaffOrReadOnlyPermission, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = PostFilterSet
    pagination_class = PostPagination
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class RetrieveDeletePostView(RetrieveModelMixin, DestroyModelMixin,
                             GenericAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsStaffOrReadOnlyPermission, )

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def delete(self, request):
        return self.destroy(request)


class ListPostTagView(ListModelMixin, GenericAPIView):
    serializer_class = PostTagSerializer
    queryset = PostTag.objects.all()

    def get(self, request):
        return self.list(request)
