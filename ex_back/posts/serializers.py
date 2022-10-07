import json
from rest_framework.serializers import (ModelSerializer,
                                        ValidationError,
                                        CharField,
                                        ImageField,
                                        SerializerMethodField)
from urllib.request import urlopen
from .models import (Post, PostTag)
from users.serializers import UserSerializer


class PostTagSerializer(ModelSerializer):
    # workaround for unique constraint during validation
    name = CharField(validators=[])
    posts_count = SerializerMethodField()

    def get_posts_count(self, obj):
        return obj.post.count()

    class Meta:
        model = PostTag
        fields = ('id', 'name', 'posts_count')
        read_only_fields = ('id', 'posts_count')


class PostSerializer(ModelSerializer):
    user = UserSerializer(required=False)
    image = ImageField(required=False)
    tags = PostTagSerializer(many=True, required=False)
    raw_tags = CharField(required=False)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', )


    def validate_tags(self, data):
        return True

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        raw_tags = validated_data.pop('raw_tags', None)

        if request and hasattr(request, "user"):
            user = request.user
            validated_data['user'] = user
            post = Post.objects.create(**validated_data)
        else:
            raise ValidationError('User not provided.')

        if raw_tags:
            raw_tags = json.loads(raw_tags)
            tags = []
            for tag_raw in raw_tags:
                name = tag_raw['name']
                tag = PostTag.objects.get_or_create(name=name)[0]
                tags.append(tag)

            post.tags.add(*tags)

        return post
