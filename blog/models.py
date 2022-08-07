from django.db import models


class PostTag(models.Model):
    title = models.CharField(max_length=14)
    slug = models.CharField(max_length=14)

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    title = models.CharField(max_length=14)
    slug = models.CharField(max_length=14)

    def __str__(self):
        return self.title


class Post(models.Model):
    thumbnail = models.ImageField(upload_to='static/media/post/')
    caption = models.CharField(max_length=32)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    tag = models.ManyToManyField('PostTag')
    category = models.ForeignKey('PostCategory', on_delete=models.CASCADE)
    description = models.TextField()
    title = models.CharField(max_length=56)
    slug = models.CharField(max_length=56)
    active = models.BooleanField(default=True)
    allow_comment = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class PostComment(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    blog = models.ForeignKey('Post', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    parent = models.ForeignKey('PostComment', on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} > {}".format(self.user, self.blog)
