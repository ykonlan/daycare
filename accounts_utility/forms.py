from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=90,label="Email")
    password = forms.CharField(label="Password",widget=forms.PasswordInput())

