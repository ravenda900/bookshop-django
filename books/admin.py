from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Book, Profile, BookSale


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(BookSale)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
