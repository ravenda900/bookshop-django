from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4


def user_img_path(instance, filename):
    return img_path("users", filename)


def book_img_path(instance, filename):
    return img_path("books", filename)


def img_path(path, filename):
    name, ext = filename.split('.')
    return "%s/%s.%s" % (path, uuid4().hex, ext)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    address = models.CharField(max_length=255)
    balance = models.FloatField(default=0)
    image = models.ImageField(upload_to=user_img_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s, %s" % (self.user.last_name, self.user.first_name)


class Book(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    quantity = models.IntegerField()
    price = models.FloatField()
    image = models.FileField(upload_to=book_img_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s) by %s" % (self.title, self.year, self.author)

    class Meta:
        ordering = ['-created_at']


class BookSale(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price_per_piece = models.FloatField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s x %s = %1.2f" % (self.book, self.quantity, self.quantity * self.price_per_piece)

    class Meta:
        ordering = ['-created_at']


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
