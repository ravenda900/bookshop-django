from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import HiddenInput
from .models import Profile

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class SignUpForm(UserCreationForm):
    birthdate = forms.DateField(widget=DateInput)
    address = forms.CharField()
    use_required_attribute = False
    error_css_class = "is-invalid"
    required_css_class = "required"

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'birthdate', 'address', 'username', 'password1', 'password2', 'is_active')
        widgets = {
            'is_active': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(SignUpForm, self).save(commit=True)
        user_profile = Profile(
            user=user,
            birthdate=self.cleaned_data['birthdate'],
            address=self.cleaned_data['address']
        )
        user_profile.save()
        return user, user_profile


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})
