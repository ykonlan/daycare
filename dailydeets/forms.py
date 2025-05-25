from django import forms
from django.forms import formset_factory
from .models import DailyDeets
from ward.models import Ward



class MealForm(forms.Form):
    meal = forms.CharField(max_length=50,required=False)
    meal_time = forms.TimeField(widget=forms.TimeInput(attrs={"type":"time"}),required=False)
    CHOICES = [
        ("",""),
        ("small","Small"),
        ("plenty","Plenty"),
        ("all","All"),
    ]
    meal_amount = forms.ChoiceField(choices=CHOICES,required=False)

    def clean(self):
        cleaned_data = super().clean()
        meal = cleaned_data.get("meal")
        meal_time = cleaned_data.get("meal_time")
        meal_amount = cleaned_data.get("meal_amount")
        fields = [meal,meal_time,meal_amount]
        filled = [bool(f) for f in fields]
        if sum(filled) < len(fields):
            raise forms.ValidationError("Please fill all fields or leave all blank")
        return cleaned_data
        
    
MealFormset = formset_factory(form=MealForm,extra=2,can_delete=False)



class NapForm(forms.Form):
    nap_start = forms.TimeField(widget=forms.TimeInput(attrs={"type":"time"}),required=False)
    nap_end = forms.TimeField(widget=forms.TimeInput(attrs={"type":"time"}),required=False)

    def clean(self):
        cleaned_data = super().clean()
        nap_start = cleaned_data.get("nap_start")
        nap_end = cleaned_data.get("nap_end")
        fields = [nap_start,nap_end]
        filled = [bool(f) for f in fields]
        if sum(filled) < len(fields):
            raise forms.ValidationError("Please fill all fields or leave all blank")
        return cleaned_data
NapFormset = formset_factory(form=NapForm,extra=2,can_delete=False)

class MedForm(forms.Form):
    med_name = forms.CharField(max_length=50,required=False)
    med_time = forms.TimeField(widget=forms.TimeInput(attrs={"type":"time"}),required=False)

    def clean(self):
        cleaned_data = super().clean()
        med_name = cleaned_data.get("med_name")
        med_time = cleaned_data.get("med_time")
        fields = [med_name,med_time]
        filled = [bool(f) for f in fields]
        if sum(filled) < len(fields):
            raise forms.ValidationError("Please fill all fields or leave all blank")
        return cleaned_data
MedFormset = formset_factory(form=MedForm,extra=2,can_delete=False)


class DailyDeetForm(forms.ModelForm):
    day_highlight = forms.CharField(max_length=150,widget=forms.Textarea,required=False)
    extra_needs = forms.CharField(max_length=100,widget=forms.Textarea,required=False)
    special_behavior = forms.CharField(max_length=100,widget=forms.TextInput,required=False)
    general_mood = forms.CharField(max_length=50,required=False)

    class Meta:
        model = DailyDeets
        fields = [
            "day_highlight",
            "extra_needs",
            "special_behavior",
            "general_mood",
        ]


class WardSelectForm(forms.ModelForm):
    class Meta:
        model = DailyDeets
        fields = ["ward_id"]
    def __init__(self,*args,class_name=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["ward_id"].queryset = Ward.objects.filter(class_name=class_name)


class GetDailyDeetsForm(forms.Form):
    ward_id = forms.ModelChoiceField(queryset=Ward.objects.all())
    date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))

    def __init__(self, *args, class_name=None, parent_id=None, **kwargs):
        super().__init__(*args,**kwargs)
        if class_name:
            self.fields["ward_id"].queryset = Ward.objects.filter(class_name=class_name)
        elif parent_id:
            self.fields["ward_id"].queryset = Ward.objects.filter(parent_id=parent_id)
        else:
            self.fields["ward_id"].queryset = Ward.objects.all()



    
