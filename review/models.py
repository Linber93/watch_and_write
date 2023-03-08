from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))
RATING = ((1, "Disliked"), (2, "Boring"), (3, "Average"), (4, "Decent"), (5, "Great"))


class Review(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_post")
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now=True)
    producer = models.CharField(max_length=100)
    actors = models.CharField(max_length=300)
    released_on = models.DateTimeField()
    excerpt = models.TextField(blank=True)
    plot = models.TextField()
    opinion = models.TextField()
    conclusion = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    rating = models.IntegerField(choices=RATING, default=3)
    likes = models.ManyToManyField(User, related_name='review_likes', blank=True)
    movie_poster = CloudinaryField('image', default='placeholder')
    review_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    comment_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.name}'



