from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254,
                            required=True,
                            label="Эл. почта",
                            widget=forms.EmailInput())

    phone = forms.CharField(max_length=20,
                            label='Телефон')

    class Meta:
        model = User
        fields = ('username', 'phone', 'first_name', 'email', 'password1', 'password2')

    def clean(self):
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Электронная почта уже занята")
        elif Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Номер телефона уже используется")
        return self.cleaned_data


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone',)
