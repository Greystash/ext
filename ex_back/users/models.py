from uuid import uuid4
from django.db.models import (
    CASCADE,
    BooleanField, CharField, EmailField,
    DateTimeField, UUIDField, URLField,
)
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self,
                    username: str | None = None,
                    email: str | None = None,
                    password: str | None = None,
                    **kwargs) -> 'User':

        user: 'User' = self.model(
            username=username,
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, password: str) -> 'User':
        user = self.create_user(username=username, password=password)
        user.is_moderator = True
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)

    # Data
    username = CharField(max_length=50, unique=True, null=True, blank=True)
    email = EmailField(max_length=255, unique=True, null=True, blank=True)
    avatar = URLField(max_length=1024, null=True, blank=True)

    # Flags
    is_moderator = BooleanField(default=False)
    is_admin = BooleanField(default=False)

    # Timestamps
    time_joined = DateTimeField(auto_now_add=True)

    objects: 'UserManager' = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return f'{self.username if self.username else self.email}'
