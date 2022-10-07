from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminPermission

from .serializers import (UpdatePasswordSerializer, UserSerializer)


User = get_user_model()


class RegisterView(APIView):
    serializer = UserSerializer

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            try:
                user = user_serializer.create(user_serializer.validated_data)
            except IntegrityError as e:
                err = str(e).split('.')[-1]
                return Response({'detail': f'User with given {err} already exists.'}, status.HTTP_400_BAD_REQUEST)

            token: 'Token' = Token.objects.create(user=user)
            return Response({'detail': 'User created.',
                             'token': token.key,
                             'user': user_serializer.data}, status.HTTP_201_CREATED)
        return Response({'detail': user_serializer.errors})


class LoginView(APIView):
    def post(self, request):
        data: dict = request.data

        try:
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)

        except KeyError:
            return Response({'detail': 'Please provide a valid credentials.'}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'Something is wrong on the server.'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not user:
            return Response({'detail': 'No user found with given credentials.'}, status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(user)
        token = Token.objects.get_or_create(user=user)[0]
        return Response({'detail': 'Successfully logged in.',
                         'token': token.key,
                         'user': user_serializer.data}, status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()

        return Response({'detail': 'Successfully logged out.'}, status.HTTP_200_OK)


class PatchView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request):
        user = self.get_object()

        user_serializer = self.serializer_class(
            data=request.data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            try:
                user_serializer.update(user, user_serializer.validated_data)
            except IntegrityError as e:
                err = str(e).split('.')[-1]
                return Response({'detail': f'User with given {err} already exists.'}, status.HTTP_400_BAD_REQUEST)

            return Response({'detail': 'Profile successfully updated.'}, status.HTTP_200_OK)
        return Response({'detail': user_serializer.errors})


class UpdatePasswordView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def post(self, request):
        user = self.get_object()
        update_password_serializer = UpdatePasswordSerializer(
            data=request.data)
        user_serializer = UserSerializer(user)

        if update_password_serializer.is_valid(raise_exception=True):
            old_password = update_password_serializer.validated_data.get(  # type: ignore
                'old_password')
            new_password = update_password_serializer.validated_data.get(  # type: ignore
                'new_password')

            if not old_password or not user.check_password(old_password):
                return Response({'detail': 'Provided password does not match. Please, provide a correct password.'},
                                status.HTTP_400_BAD_REQUEST)
            if not new_password:
                return Response({'detail': 'Please provide a new password.'},
                                status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            # Update user's token.
            Token.objects.get(user=user).delete()
            token = Token.objects.create(user=user)

            return Response({'detail': 'Password successfully changed.',
                             'token': token.key,
                             'user': user_serializer.data}, status.HTTP_200_OK)

        return Response({'detail': update_password_serializer.errors})


class UpdateUserGroupsView(APIView):
    permission_classes = (IsAdminPermission,)

    def post(self, request):
        user_id = request.data.get('user_id', None)
        is_moderator = request.data.get('is_moderator', False)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'Such user does not exist.'},
                            status.HTTP_400_BAD_REQUEST)

        user.is_moderator = is_moderator  # type: ignore
        user.save()
        return Response({'detail': 'User permissions successfully updated.'},
                        status.HTTP_200_OK)


class GetUsersView(ListModelMixin, GenericAPIView):
    permission_classes = (IsAdminPermission, )
    queryset = User.objects.filter(is_admin=False)
    serializer_class = UserSerializer

    def get(self, request):
        return self.list(request)
