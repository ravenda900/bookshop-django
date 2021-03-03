import os
from django.db import models
from django.contrib.auth.models import User
from composite_field import CompositeField
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


class AddressField(CompositeField):
    barangay = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    address = AddressField()
    balance = models.FloatField(default=0)
    image = models.ImageField(upload_to=user_img_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # description = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    quantity = models.IntegerField()
    price = models.FloatField()
    image = models.FileField(upload_to=book_img_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

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
        return self.get_id_display()

    class Meta:
        ordering = ['-created_at']


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
