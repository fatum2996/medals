from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Medal_To_Moderate

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

# posts/forms.py

class MedalForm(forms.ModelForm):

    class Meta:
        model = Medal_To_Moderate
        fields = ['name', 'photo', 'photo_second', 'location', 'org']
        labels = {
            "name": "Название соревнования",
            "photo": "Фото медали",
            "photo_second": "Фото реверса",
            "location": "Место проведения (город)",
            "org": "Организатор",
        }
