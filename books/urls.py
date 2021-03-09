from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('sell-book', views.sell_book, name='sell_book'),
    path('add-balance', views.add_balance, name='add_balance'),
    path('posted-books', views.posted_books, name='posted_books'),
    path('sold-books', views.sold_books, name='sold_books')
]