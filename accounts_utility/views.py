from django.shortcuts import render,redirect
from django.views import View
from .forms import LoginForm
from django.contrib.auth import login,authenticate
from django.contrib import messages


class login_page_render(View):
    def get(self,request):
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request=request,email=form.cleaned_data.get("email"),password=form.cleaned_data.get("password"))
            if user:
                login(request,user)
                return redirect("dashboard")
            else:
                messages.error(request,"Invalid email or password") 
        return render(request,"login.html",{"form":form})
    
class dashboard_render(View):
    def get(self,request):
        return render(request,"dashboard.html")
        
        