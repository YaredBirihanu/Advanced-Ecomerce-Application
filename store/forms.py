from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject','rating','review']