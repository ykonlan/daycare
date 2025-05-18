from django import forms
from .models import Ward,Allergies
from django.forms import inlineformset_factory


class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergies
        exclude = ["ward_id"]
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.required = False

class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ["name","date_of_birth","parent_id","class_name"]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type":"date"})}

AllergyFormSet = inlineformset_factory(parent_model=Ward,model=Allergies,form=AllergyForm,extra=2,can_delete=False)

        
