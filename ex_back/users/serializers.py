import re
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (ModelSerializer,
                                        Serializer,
                                        CharField,
                                        ValidationError as SerializerValidationError,)


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'email',
            'username', 'avatar', 'password',
            'is_moderator', 'is_admin'
        ]
        read_only_fields = (
            'id', 'time_joined', 'is_moderator', 'is_admin')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        email_match = re.compile(
            r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
        if not value:
            return None
        if not re.fullmatch(email_match, value):
            raise SerializerValidationError('Please provide a valid email.')
        return value

    def validate_username(self, value):
        username_match = re.compile(
            r"^(?=.{1,50}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$")
        if not value:
            return None
        if not re.fullmatch(username_match, value):
            raise SerializerValidationError(
                'Username can only contain lower and uppercase letters, digits and few special symbols.')
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        # Making sure at least 1 login field provided.
        if not validated_data.get('username') and not validated_data.get('email'):
            raise SerializerValidationError(
                'Username or email must be provided.')
        return get_user_model().objects.create_user(**dict(validated_data))  # type: ignore

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        if instance.check_password(password):
            return super().update(instance, validated_data)

        raise SerializerValidationError(
            'Password is incorrect, please provide a valid password.')


class UpdatePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
