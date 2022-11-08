from django.forms import ModelForm
from django import forms

from .models import *

class GForm(ModelForm):
    class Meta:
        model = Goods
        fields = ("title", "content", "price", "image")
