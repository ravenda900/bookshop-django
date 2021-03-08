import sys

sys.path.insert(0, '/bookshop-proj')
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookshop_proj.settings')

import django

django.setup()

from django.contrib.auth.models import User
from books.models import Book, BookSale, Profile
from faker import Faker
import random

faker = Faker()


def seed():
    print("Seeding superuser...")
    User.objects.create_superuser(username="admin", password="admin")
    print("Superuser seeding completed.")

    print("Seeding user...")
    for i in range(20):
        first_name = faker.first_name()
        last_name = faker.last_name()
        user = User.objects.create_user(
            username="user%d" % (i + 1),
            password=first_name,
            email=first_name.lower() + '@' + last_name.lower() + '.com',
            first_name=first_name,
            last_name=last_name
        )
        print("%s seeded" % user)
    print("User seeding completed.")

    print("Seeding user profile...")
    for i in range(20):
        profile = Profile.objects.create(
            birthdate=faker.past_date(),
            address=faker.address(),
            balance=round(random.uniform(0, 50000), 2),
            image="https://loremflickr.com/200/200/person?random=%d&lock=%d" % (i + 1, i + 1),
            email_confirmed=faker.boolean(),
            user=User.objects.get(pk=(i + 2))
        )
        print("%s seeded" % profile)
    print("User profile seeding complete")

    print("Seeding book...")
    for i in range(50):
        book = Book.objects.create(
            seller=random.choice(User.objects.all()),
            title=faker.sentence(nb_words=5),
            author=faker.name(),
            description=faker.sentence(nb_words=5),
            genre=faker.word(),
            year=random.randint(1990, 2021),
            quantity=random.randint(1, 30),
            price=round(random.uniform(100, 1000), 2),
            image="https://loremflickr.com/420/225/bookcover?random=%d&lock=%d" % (i + 1, i + 1)
        )
        print("%s seeded" % book)
    print("Book seeding completed.")

    print("Seeding book sale...")
    for i in range(50):
        booksale = BookSale.objects.create(
            buyer=random.choice(User.objects.all()),
            book=random.choice(Book.objects.all()),
            price_per_piece=round(random.uniform(100, 1000), 2),
            quantity=random.randint(1, 30)
        )
        print("%s seeded" % booksale)
    print("Book sale seeding completed.")
    print("All seeders completed")


if __name__ == '__main__':
    print("Seeding data. Please wait.")
    seed()
    print("Seeding complete")
