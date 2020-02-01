from django import forms
from .models import User
from .models import Diary
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('email', 'password')
    def clean(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        password=str(password)
        if not (5 <= len(password) <= 8) :
            raise forms.ValidationError("パスワードは5~8文字で入力してください")

class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('email', 'password')
    def clean(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        data=User.objects.all().filter(email=email, password=password).exists()

class DiaryAddForm(forms.ModelForm):
    class Meta:
        model=Diary
        fields=('diary',)
    def clean(self):
        diary=self.cleaned_data.get('diary')
        if not (len(diary)<=500):
            raise forms.ValidationError("500文字以内で入力してください。")
