from django.shortcuts import render,redirect
from django.views import View
from .models import Ward
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import WardForm,AllergyFormSet
from django.http import Http404
from .models import Allergies




class GetWardView(LoginRequiredMixin,View):
    login_url = "/login/"
    redirect_field_name = "next"
    def get(self,request,ward_id=None):
        user = request.user
        is_a_parent =user.groups.filter(name="parents").exists()
        is_a_staff =user.groups.filter(name="staff").exists()
        if ward_id:
            ward = Ward.objects.select_related("parent_id").filter(id=ward_id).first()
            if not ward:
                raise Http404("Ward not found!")
            allergies = Allergies.objects.filter(ward_id=ward)
            if user.is_superuser:
                return render(request,"ward-details.html",{"ward":ward,"allergies":allergies})
            elif is_a_parent:
                if ward.parent_id_id != user.id:
                    return redirect("dashboard")
            elif is_a_staff:
                if user.staff_profile.class_name != ward.class_name:
                    return redirect("dashboard")
            else:
                return redirect("dashboard")
            return render(request,"ward-details.html",{"ward":ward,"allergies":allergies})
        else:
            if user.is_superuser:
                wards = Ward.objects.all()
                return render(request,"my-wards.html",{"wards":wards})
            elif is_a_parent:
                wards = Ward.objects.filter(parent_id=user.id)
                return render(request,"my-wards.html",{"wards":wards})
            elif is_a_staff:
                wards = Ward.objects.filter(class_name=user.staff_profile.class_name)
                return render(request,"my-wards.html",{"wards":wards})
            else:
                return redirect("dashboard")
            
class AddWardView(LoginRequiredMixin,View):
    login_url = "/login/"
    redirect_field_name = "next"
    def get(self,request):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        form = WardForm()
        allergies = AllergyFormSet()
        return render(request,"add-ward.html",{"form":form,"allergy_form":allergies})
    
    def post(self,request):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        form = WardForm(request.POST)
        if form.is_valid():
            ward = form.save()
            allergies = AllergyFormSet(request.POST,instance=ward)
            if allergies.is_valid():
                allergies.save()
            else:
                return render(request,"add-ward.html",{"form":form,"allergy_form":allergies})
        else:
            allergies = AllergyFormSet(request.POST)
            return render(request,"add-ward.html",{"form":form,"allergy_form":allergies})
        return redirect("add-ward")
    
class PatchWardView(LoginRequiredMixin,View):
    login_url = "/login/"
    redirect_field_name = "next"
    def get(self,request,ward_id):
        user = request.user 
        if not user.is_superuser:
            return redirect("dashboard")
        ward = get_object_or_404(Ward,id=ward_id)
        form = WardForm(instance=ward)
        allergies = AllergyFormSet(instance=ward)
        return render(request,"edit-ward.html",{"form":form,"allergies":allergies,"ward":ward})
    
    def post(self,request,ward_id):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        ward = get_object_or_404(Ward,id=ward_id)
        form = WardForm(request.POST,instance=ward)
        allergies = AllergyFormSet(request.POST,instance=ward)
        if form.is_valid() and allergies.is_valid():
            form.save()
            allergies.save()
            return redirect("edit-wards",ward_id=ward.id)
        return render(request,"edit-ward.html",{"form":form,"allergies":allergies,"ward":ward})
    

class DeleteWardView(LoginRequiredMixin,View):
    login_url = "/login/"
    redirect_field_name = "next"
    def post(self,request,ward_id):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        ward = get_object_or_404(Ward,id=ward_id)
        ward.delete()
        return redirect("view-wards")
        
            


                


