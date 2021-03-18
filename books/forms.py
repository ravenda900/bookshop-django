from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Book, BookSale


class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs['format'] = '%Y-%m-%d'
        super().__init__(**kwargs)


class SignUpForm(UserCreationForm):
    birthdate = forms.DateField(widget=DateInput)
    address = forms.CharField()
    use_required_attribute = False
    error_css_class = 'is-invalid'
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'birthdate', 'address', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError('Can\'t create User and UserProfile without database save')

        user = super(SignUpForm, self).save(commit=False)
        last_inserted_id = User.objects.last().id
        user.profile.image = "https://loremflickr.com/420/225/bookcover?random=%d&lock=%d" % (last_inserted_id + 1, last_inserted_id + 1)
        user.is_active = False

        if commit:
            user.save()

        user_profile = Profile(
            user=user,
            birthdate=self.cleaned_data['birthdate'],
            address=self.cleaned_data['address']
        )
        user_profile.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})


class SellBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'description',
            'genre',
            'year',
            'quantity',
            'price',
        ]


class AddBalanceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['balance']
