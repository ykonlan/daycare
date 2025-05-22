from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import StaffForm
from accounts_utility.models import CustomUserModel
from .models import StaffProfile
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class AddStaffView(LoginRequiredMixin,View):
    login_url = "/login/"
    redirect_field_name = "next"
    def get(self,request):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        form = StaffForm()
        return render(request,"add-staff.html",{"form":form})
    
    def post(self,request):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        form = StaffForm(request.POST)
        if form.is_valid():
            user_phone = form.cleaned_data.get("user_phone")
            email = form.cleaned_data.get("email")
            name = form.cleaned_data.get("name")
            class_name = form.cleaned_data.get("class_name")
            
            user = CustomUserModel(user_phone=user_phone,email=email,name=name)
            group = Group.objects.get(name="staff")
            user.save()
            user.groups.add(group)
            
        
            staff_profile = StaffProfile(staff_id=user,class_name=class_name)
            staff_profile.save()
        return redirect("add-staff")
    

class EditStaffView(LoginRequiredMixin,View):
    login_url = "/login/"
    redirect_field_name = "next"
    def get(self,request,staff_id):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        staff = get_object_or_404(CustomUserModel,id=staff_id)
        staff_profile = StaffProfile.objects.get(staff_id=staff_id)
        initial = {
            "name": staff.name,
            "user_phone": staff.user_phone,
            "email": staff.email,
            "class_name": staff_profile.class_name,
        }
        form = StaffForm(instance=staff,initial=initial)
        return render(request,"edit-staff.html",{"form":form,"staff_id":staff_id})
    
    def post(self,request,staff_id):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        staff = get_object_or_404(CustomUserModel,id=staff_id)
        staff_profile = StaffProfile.objects.get(staff_id=staff_id)
        form = StaffForm(instance=staff_profile,data=request.POST)
        if form.is_valid():
            staff.name = form.cleaned_data.get("name")
            staff.user_phone = form.cleaned_data.get("user_phone")
            staff.email = form.cleaned_data.get("email")
            staff.save()
            # Update staff profile fields
            staff_profile.class_name = form.cleaned_data.get("class_name")
            staff_profile.save()
            return redirect("edit-staff", staff_id=staff_id)
        else:
            return render(request,"edit-staff.html",{"form":form,"staff_id":staff_id})
        
class GetStaffView(LoginRequiredMixin,View):
    login_url = "/login/"
    redirect_field_name = "next"
    def get(self,request,staff_id=None):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        if staff_id:
            staff_profile = StaffProfile.objects.select_related("staff_id").get(staff_id=staff_id)
            return render(request,"view-staff-details.html",{"class_name":staff_profile.class_name,"staff":staff_profile.staff_id})
        else:
            staff_profiles = StaffProfile.objects.select_related("staff_id").all()
            return render(request,"view-staff.html",{"staff_profiles":staff_profiles})
        

class DeleteStaffView(LoginRequiredMixin,View):
    login_url = "/login/"
    redirect_field_name = "next"
    def post(self,request,staff_id):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        staff = get_object_or_404(CustomUserModel,id=staff_id)
        staff.delete()
        return redirect("view-staff")

    







        
