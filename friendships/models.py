from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    # from_user 指向 to_user
    from_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        # 作为区分，使用user.following_friendship_set
        related_name='following_friendship_set',
    )

    to_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        # 作为区分，使用user.follower_friendship_set
        related_name='follower_friendship_set',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            # 获取我关注的所有人，按照关注时间排序
            ('from_user_id', 'created_at'),
            # 获得关注我的所有人，按照关注时间排序
            ('to_user_id', 'created_at'),
        )
        unique_together = (('from_user_id', 'to_user_id'),)
        ordering = ('-created_at',)

    def __str__(self):
        return '{} followed {}'.format(self.from_user_id, self.to_user_id)