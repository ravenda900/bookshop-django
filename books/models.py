from django.db import models
from django.contrib.auth.models import User
from composite_field import CompositeField


class AddressField(CompositeField):
    barangay = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    address = AddressField()
    balance = models.FloatField()
    avatar = models.ImageField(upload_to='avatars')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_id_display()


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    quantity = models.IntegerField()
    price = models.FloatField()
    image = models.FileField(upload_to='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_id_display()

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
