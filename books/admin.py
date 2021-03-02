from django.contrib import admin

from .models import Book, Profile, BookSale
admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(BookSale)
