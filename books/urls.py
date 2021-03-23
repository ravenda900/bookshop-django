from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('sell-book', views.sell_book, name='sell_book'),
    path('book/<int:id>/detail', views.book_detail, name='book_detail'),
    path('add-balance', views.add_balance, name='add_balance'),
    path('books-for-sale', views.books_for_sale, name='books_for_sale'),
    path('purchased-books', views.purchased_books, name='purchased_books'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('cart-items', views.cart_items, name='cart_items'),
    path('add-items-to-cart/<int:book_item>', views.add_items_to_cart, name="add_items_to_cart"),
    path('cancel-items', views.cancel_items, name="cancel_items"),
    path('checkout', views.checkout, name='checkout')
]