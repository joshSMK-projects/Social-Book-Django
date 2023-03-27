from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    # Used for display in the admin panel
    def __str__(self):
        return self.user.username

# Posts are not tied to the users
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(max_length=250)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} - {self.caption}'
    

# Ties a post to a username
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.username} liked {Post.objects.get(id=self.post_id).user}\'s post'

# Ties the username of the follower and the username of the profile who is following
class FollowersCount(models.Model):
    following_user = models.CharField(max_length=100)
    followed_user = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.following_user} follows {self.followed_user}'