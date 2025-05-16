from django.shortcuts import render,redirect
from django.views import View
from .models import Ward
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin



class WardView(LoginRequiredMixin,View):
    login_url = "/login/"
    redirect_field_name = "next"
    def get(self,request,ward_id=None):
        is_a_parent = request.user.groups.filter(name="parents").exists()
        is_a_staff = request.user.groups.filter(name="staff").exists()
        user = request.user
        if ward_id:
            ward = get_object_or_404(Ward,id=ward_id)
            if is_a_parent and is_a_staff:
                if ward.parent_id_id != user.id or ward.class_name != request.user.staff_profile.class_name:
                    return redirect("all-wards")
            if is_a_parent:
                if ward.parent_id_id != user.id:
                    return redirect("all-wards")
            if is_a_staff:
                if request.user.staff_profile.class_name != ward.class_name:
                    return redirect("all-wards")
        return render(request,"ward-details.html",{"ward":ward})
                


