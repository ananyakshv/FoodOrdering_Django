from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# ContactForm (as you already have)
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()

# RegistrationForm (new form)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Optional: Add custom validation to ensure passwords match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        password_confirm = cleaned_data.get("password2")

        if password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return cleaned_data
