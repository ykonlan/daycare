from django import forms
from .models import StaffProfile


class StaffForm(forms.ModelForm):
    name = forms.CharField(max_length=100,label="Name")
    user_phone = forms.CharField(max_length=15,label="Phone")
    email = forms.EmailField(max_length=100,label="Email") 
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    class Meta:
        model = StaffProfile
        fields = ["class_name"]

