from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ProductReview

class SignupForm(UserCreationForm):
    full_names = forms.CharField(max_length=50,required=True)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
    address = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields=('full_names','mobile', 'address', 'username', 'password1', 'password2')

class ReviewAdd(forms.ModelForm):
    class Meta:
        model=ProductReview
        fields=('review_text','review_rating')