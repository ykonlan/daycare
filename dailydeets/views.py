from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db import IntegrityError
from .forms import DailyDeetForm,MealFormset,NapFormset,MedFormset,WardSelectForm
from django.shortcuts import get_object_or_404
from staff.models import StaffProfile
from ward.models import Ward
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import DailyDeets
from django.utils import timezone

class FillDailyDeetForm(LoginRequiredMixin,View):
    def post(self,request,ward_id):
        ward_select = WardSelect()
        user = request.user
        if not user.groups.filter(name="staff").exists():
            return redirect("dashboard")
        class_name = StaffProfile.objects.get(staff_id=user.id).class_name
        print(request.POST)
        form = DailyDeetForm(request.POST)
        meal_formset = MealFormset(request.POST,prefix="meals")
        nap_formset = NapFormset(request.POST,prefix="naps")
        med_formset = MedFormset(request.POST,prefix="meds")
        today = timezone.now().date()
        ward = get_object_or_404(Ward,id=ward_id)
        daily_deet_instance = DailyDeets.objects.filter(ward_id=ward,date=today).first()
        if daily_deet_instance:
            form = DailyDeetForm(request.POST,instance=daily_deet_instance)
        if form.is_valid() and meal_formset.is_valid() and nap_formset.is_valid() and med_formset.is_valid():
            ward_class = ward.class_name
            if ward_class != class_name:
                raise PermissionDenied("You do not have permission to submit details for this ward.")
            meals = []
            for meal_form in meal_formset:
                if meal_form.cleaned_data and any(meal_form.cleaned_data.values()):
                    meals.append({"meal":meal_form.cleaned_data.get("meal"),
                        "meal_time":meal_form.cleaned_data.get("meal_time").strftime("%H:%M"),
                        "meal_amount":meal_form.cleaned_data.get("meal_amount")
                        })
            naps = []
            for nap_form in nap_formset:
                if nap_form.cleaned_data and any(nap_form.cleaned_data.values()):
                    naps.append(
                        {"nap_start":nap_form.cleaned_data.get("nap_start").strftime("%H:%M"),
                        "nap_end":nap_form.cleaned_data.get("nap_end").strftime("%H:%M")}
                        )
            meds = []
            for med_form in med_formset:
                if med_form.cleaned_data and any(med_form.cleaned_data.values()):
                    meds.append(
                        {"med_name":med_form.cleaned_data.get("med_name"),
                        "med_time":med_form.cleaned_data.get("med_time").strftime("%H:%M")}
                        )
            daily_deet = form.save(commit=False)
            daily_deet.ward_id = ward
            daily_deet.medication = meds
            daily_deet.naps = naps
            daily_deet.meals = meals
            try:
                daily_deet.save()
                messages.success(request,"Form filled successfully")
                return redirect("fill-forms")
            except IntegrityError:
                messages.error(request,"You can only save a form for a child once a day. Forms can be edited after saving though.")
                return render(request,"fill-daily-deets.html",{"form":form,"meals":meal_formset,"naps":nap_formset,"meds":med_formset,"ward":ward,"today":today})
        else:
            return render(request,"fill-daily-deets.html",{"form":form,"meals":meal_formset,"naps":nap_formset,"meds":med_formset,"ward":ward,"today":today,"ward_select":ward_select})


        
        
class WardSelect(LoginRequiredMixin,View):
    def get(self,request):
        print("In WardSelect view")
        class_name = StaffProfile.objects.get(staff_id=request.user.id).class_name
        ward_select = WardSelectForm(class_name=class_name)
        return render(request,"fill-daily-deets.html",{"ward_select":ward_select})
    
    def post(self,request):
        class_name = StaffProfile.objects.get(staff_id=request.user.id).class_name
        ward_select = WardSelectForm(request.POST,class_name=class_name)
        if ward_select.is_valid():
            ward = ward_select.cleaned_data.get("ward_id")
            today = timezone.now().date()
            daily_deet = DailyDeets.objects.filter(ward_id=ward,date=today)
            class_name = StaffProfile.objects.get(staff_id=request.user.id).class_name
            if not class_name:
                return redirect("dashboard")
            if not daily_deet.exists():
                form = DailyDeetForm()
                ward_form = WardSelectForm(class_name=class_name)
                naps = NapFormset(prefix="naps")
                meals = MealFormset(prefix="meals")
                meds = MedFormset(prefix="meds")
            else:
                daily_deet = daily_deet.first()
                form = DailyDeetForm(instance=daily_deet)
                ward_form = WardSelectForm(initial={"ward_id":ward.id})
                naps = NapFormset(initial=daily_deet.naps,prefix="naps")
                meals = MealFormset(initial=daily_deet.meals,prefix="meals")
                meds = MedFormset(initial=daily_deet.medication,prefix="meds")
            return render(request,"fill-daily-deets.html",{"ward_select":ward_form,"form":form,"naps":naps,"meals":meals,"meds":meds,"ward":ward,"today":today})
        else:
            return render(request,"fill-daily-deets.html",{"ward_select":ward_select})
    
        
          