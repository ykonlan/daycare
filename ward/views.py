from django.shortcuts import render,redirect
from django.views import View
from .models import Ward
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin



class WardView(LoginRequiredMixin,View):
    login_url = "/login/"
    redirect_field_name = "next"
    def get(self,request,ward_id=None):
        user = request.user
        is_a_parent =user.groups.filter(name="parents").exists()
        is_a_staff =user.groups.filter(name="staff").exists()
        if ward_id:
            ward = get_object_or_404(Ward,id=ward_id)
            if user.is_superuser:
                return render(request,"ward-details.html",{"ward":ward})
            elif is_a_parent:
                if ward.parent_id_id != user.id:
                    return redirect("dashboard")
            elif is_a_staff:
                if user.staff_profile.class_name != ward.class_name:
                    return redirect("dashboard")
            else:
                return redirect("dashboard")
            return render(request,"ward-details.html",{"ward":ward})
        else:
            if is_a_parent:
                wards = Ward.objects.filter(parent_id=user.id)
                return render(request,"my-wards.html",{"wards":wards})
            elif is_a_staff:
                wards = Ward.objects.filter(class_name=user.staff_profile.class_name)
                return render(request,"my-wards.html",{"wards":wards})
            elif user.is_superuser:
                wards = Ward.objects.all()
                return render(request,"my-wards.html",{"wards":wards})
            else:
                return redirect("dashboard")
            


                


