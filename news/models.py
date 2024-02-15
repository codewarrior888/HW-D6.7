from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.urls import reverse


class Author(models.Model):
    userAuthor = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.IntegerField(default=0)

    def update_rating(self):
        post_ratings = self.post_set.aggregate(post_rating_sum=models.Sum('post_rating'))['post_rating_sum'] or 0

        comment_ratings = self.userAuthor.comment_set.\
                                   aggregate(comment_rating_sum=models.Sum('comment_rating'))['comment_rating_sum'] or 0

        self.authorRating = post_ratings * 3 + comment_ratings
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    # subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    article = 'AR'
    news = 'NW'

    POST_GENRE = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_genre = models.CharField(max_length=2, choices=POST_GENRE)
    post_title = models.CharField(max_length=128)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)
    post_time = models.DateTimeField(auto_now_add=True)

    category = models.ManyToManyField(Category, through='PostCategory')

    def get_absolute_url(self):
        post_genre = 'news' if self.post_genre == 'NW' else 'articles'
        return reverse(f'{post_genre}_list')

    def preview(self):
        words = self.post_text.split()
        preview_text = ' '.join(words[:20])
        return f"{preview_text}..."

    def like(self):
        self.post_rating = F('post_rating') + 1
        self.save()

    def dislike(self):
        self.post_rating = F('post_rating') - 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating = F('comment_rating') + 1
        self.save()

    def dislike(self):
        self.comment_rating = F('comment_rating') - 1
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
