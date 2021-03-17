from django.contrib.auth.models import User
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
from .forms import SignUpForm, SellBookForm, AddBalanceForm


def home(request):
    return render(request, 'home.html', {
        'books': Book.objects.all()
    })


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

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

            messages.success(request, 'Please confirm your email to complete registration.')

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
        login(request, user)
        messages.success(request, 'Your account have been confirmed.')
    else:
        messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')

    return redirect('home')


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

            return redirect('posted_books')
    else:
        form = SellBookForm()
    return render(request, 'sell_book.html', {'form': form})


def posted_books(request):
    books = Book.objects.filter(seller=request.user)

    return render(request, 'posted_books.html', {'posted_books': books})


def sold_books(request):
    books = Book.objects.filter(seller=request.user)

    return render(request, 'sold_books.html', {'sold_books': books})


def add_balance(request):
    if request.method == 'POST':
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            user = request.user
            user.profile.balance = user.profile.balance + float(request.POST.get('balance'))
            user.profile.save()
            messages.success(request, "Successfully added ₱%s balance to your account" % request.POST.get('balance'))
            messages.error(request, "Your total amount is ₱%1.2f" % user.profile.balance, 'danger')

            return redirect('add_balance')
    else:
        form = AddBalanceForm()
    return render(request, 'add_balance.html', {'form': form})

