from django.shortcuts import render,redirect
from django.views import View
from .forms import LoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from ward.models import Ward, Classes
from staff.models import StaffProfile


class login_page_render(View):
    def get(self,request):
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request=request,username=form.cleaned_data.get("email"),password=form.cleaned_data.get("password"))
            if user:
                login(request,user)
                if request.POST.get("next") or request.GET.get("next"):
                    return redirect(request.POST.get("next") or request.GET.get("next"))
                else:
                    if user.is_superuser:
                        return render(request, "admin-dashboard.html")
            else:
                messages.error(request,"Invalid email or password") 
        return render(request,"login.html",{"form":form})
    
class dashboard_render(View):
    def get(self,request):
        if request.user.is_superuser:
            ward_pop = Ward.objects.count()
            staff_pop = StaffProfile.objects.count()
            class_count = Classes.objects.count()
            return render(request,"admin-dashboard.html",{"ward_pop": ward_pop, "staff_pop": staff_pop, "class_count": class_count})
    
class logout_view(View):
    def post(self,request):
        logout(request)
        return redirect("login")

        
        