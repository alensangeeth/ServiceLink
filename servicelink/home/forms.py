from django import forms
from django.contrib.auth.hashers import make_password
from .models import User,ServiceProvider, Category
from django.contrib.auth.forms import UserCreationForm

from django import forms

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  # Hide password input
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # Make address field like others

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'phone', 'address', 'city', 'role']

    def save(self, commit=True):
        """Override save method to hash the password"""
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Hash password
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 100%;'})
    )

class ServiceProviderForm(forms.Form):
    company_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
    category_id = forms.ChoiceField(choices=[], required=True)  # Set dynamically

    def __init__(self, *args, **kwargs):
        super(ServiceProviderForm, self).__init__(*args, **kwargs)
        # ✅ Populate category choices
        categories = Category.objects.all()
        self.fields['category_id'].choices = [("", "-- Select Category --")] + [
            (category.category_id, category.category_name) for category in categories
        ]
