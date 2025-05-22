from django import forms
from accounts_utility.models import CustomUserModel

class ParentForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ["name","user_phone","email"]

