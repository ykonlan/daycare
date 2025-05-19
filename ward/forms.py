from django import forms
from .models import Ward,Allergies
from django.forms import BaseInlineFormSet,inlineformset_factory
from django.core.exceptions import ValidationError


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

class ReqAllergyFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not hasattr(form,"cleaned_data"):
                continue
            if not any(form.cleaned_data.values()):
                continue
            required = ["allergy_name","allergy_reaction","allergy_severity"]
            missing = [f for f in required if not form.cleaned_data.get(f)]
            if missing:
                raise ValidationError("Allergy forms attempted must be completed")
            
AllergyFormSet = inlineformset_factory(Ward,Allergies,fields=["allergy_name","allergy_reaction","allergy_severity"],extra=2,formset=ReqAllergyFormSet,can_delete=False)
            



        
