from accounts.api.serializers import UserSerializerForTweet
from accounts.api.serializers import UserSerializerForComment
from rest_framework import serializers
from tweets.models import Tweet
from comments.api.serializers import CommentSerializer


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializerForTweet()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')


class TweetSerializerForCreate(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)

    # 执行TweetSerializerForCreate.save()时 会自动调用create
    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet


class TweetSerializerWithComments(serializers.ModelSerializer):
    user = UserSerializerForComment()
    # <HOMEWORK> 使用 serialziers.SerializerMethodField 的方式实现 comments
    comments = CommentSerializer(source='comment_set', many=True)

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'comments', 'created_at', 'content')