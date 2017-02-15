from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django import forms
# from .models import User as usr


User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# class UserInfForm(forms.ModelForm):
#    class Meta:
#        model = usr
#        fields = ['photo', 'username', 'first_name', 'last_name', 'python3', 'cpp']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        return super(UserLoginForm, self).clean(*args, **kwargs)


class TaskForm(forms.Form):
    code = forms.CharField(widget = forms.Textarea(attrs={'placeholder': 'enter code here', 'cols': '70'}))

    def clean(self, *args, **kwargs):
        code = self.cleaned_data.get('code')
        return super(TaskForm, self).clean(*args, **kwargs)
