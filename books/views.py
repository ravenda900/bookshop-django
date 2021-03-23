from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth import login
from django.utils.encoding import force_text
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib import messages
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, SellBookForm, AddBalanceForm, UpdateProfileForm


def home(request):
    return render(request, 'home.html', {
        'books': Book.objects.all()
    })


def signup(request):
    if request.user.is_authenticated:
        raise Http404("Cannot access this page.")

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, 'Please confirm your email to complete the registration.')

            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.profile.save()
        user.save()
        messages.success(request, 'Your account has been confirmed. Please login to continue.')
        return redirect('login')
    else:
        messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used/incorrect')

    return redirect('home')


@login_required(login_url="/login")
def sell_book(request):
    if request.method == 'POST':
        form = SellBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            last_inserted_id = Book.objects.first().id
            book.seller = request.user
            book.image = "https://loremflickr.com/420/225/bookcover?random=%d&lock=%d" % (last_inserted_id, last_inserted_id)
            book.save()

            messages.success(request, '%s has been posted' % book)

            return redirect('books_for_sale')
    else:
        form = SellBookForm()
    return render(request, 'sell_book.html', {'form': form})


@login_required(login_url="/login")
def books_for_sale(request):
    books = Book.objects.filter(seller=request.user)

    return render(request, 'books.html', {
        'books': books,
        'title': 'Books for Sale'
    })


@login_required(login_url="/login")
def purchased_books(request):
    books = Book.objects.filter(seller=request.user)

    return render(request, 'books.html', {'books': books,
        'title': 'Purchased Books'
    })


@login_required(login_url="/login")
def add_balance(request):
    if request.method == 'POST':
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            user = request.user
            user.profile.balance = user.profile.balance + float(request.POST.get('balance'))
            user.profile.save()
            messages.success(request, "Successfully added ₱%s balance to your account" % request.POST.get('balance'))
            messages.success(request, "Your total amount is ₱%1.2f" % user.profile.balance)

            return redirect('add_balance')
    else:
        form = AddBalanceForm()
    return render(request, 'add_balance.html', {'form': form})


@login_required(login_url="/login")
def profile(request, username):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)

        if form.is_valid():
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            user.profile.address = request.POST.get('address')
            user.profile.birthdate = request.POST.get('birthdate')
            user.profile.save()

            messages.success(request, 'Successfully updated profile')
    else:
        form = UpdateProfileForm()
        if request.user.username != username:
            raise Http404("Cannot access this page.")
    return render(request, 'profile.html', {'form': form})


@login_required(login_url="/login")
def book_detail(request, id):
    book = Book.objects.get(pk=id)

    return render(request, 'book_detail.html', {
        'book': book
    })


@login_required(login_url="/login")
def cart_items(request):
    book_items = request.session.get('book_items', [])
    books = []
    total_price = 0

    book_list = Book.objects.filter(pk__in=book_items)
    for book in book_list:
        count = book_items.count(book.id)
        books.append({
            'count': book_items.count(book.id),
            'model': book
        })
        total_price += count * book.price

    return render(request, 'cart_items.html', {
        'books': books,
        'total_price': total_price
    })


@login_required(login_url="/login")
@csrf_exempt
def add_items_to_cart(request, book_item):
    book_items = request.session.get('book_items', [])
    book_items.append(book_item)
    request.session['book_items'] = book_items

    return JsonResponse({'success': 'Successfully added item to cart'}, status=200)

@login_required(login_url="/login")
def cancel_items(request):
    request.session['book_items'] = []
    return redirect('home')

@login_required(login_url="/login")
def checkout(request):
    return render(request, 'checkout.html')



