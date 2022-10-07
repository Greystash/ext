from uuid import uuid4
from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    SET_NULL,
    Model,
    UUIDField,
    CharField,
    TextField,
    ForeignKey,
    DateTimeField,
    ImageField,
    URLField,
    ManyToManyField,
)


class Post(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)

    user = ForeignKey(get_user_model(), SET_NULL, null=True)
    title = CharField(max_length=255, blank=True)
    body = TextField(blank=True)
    datetime = DateTimeField(auto_now_add=True)
    image = ImageField(null=True, blank=True)

    class Meta:
        ordering = ('-datetime', )


class PostTag(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)

    post = ManyToManyField(Post, related_name='tags')
    name = CharField(max_length=50, unique=True)
