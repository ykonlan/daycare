from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import ParentForm
from accounts_utility.models import CustomUserModel
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.db.models import Q



class AddParentView(LoginRequiredMixin,View):
    login_url = ""
    redirect_field_name = "next"
    def get(self,request):
        user = request.user
        if not user.is_superuser:
            return redirect("dashboard")
        form = ParentForm()
        return render(request,"add-parents.html",{"form":form})
    
    def post(self,request):
         user = request.user
         if not user.is_superuser:
             return redirect("dashboard")
         form = ParentForm(request.POST)
         if form.is_valid():
             user_phone = form.cleaned_data.get("user_phone")
             email = form.cleaned_data.get("email")
             name = form.cleaned_data.get("name")
            
             user = CustomUserModel(user_phone=user_phone,email=email,name=name)
             user.save()
             group = Group.objects.get(name="parents")
             user.groups.add(group)
            
             return redirect("add-parent")
         else:
             return render(request,"add-parents.html",{"form":form})
    

class EditParentView(LoginRequiredMixin,View):
     login_url = ""
     redirect_field_name = "next"
     def get(self,request,parent_id):
         user = request.user
         if not user.is_superuser:
             return redirect("dashboard")
         parent = get_object_or_404(CustomUserModel,id=parent_id)
         initial = {
             "name": parent.name,
             "user_phone": parent.user_phone,
             "email": parent.email,
         }
         form = ParentForm(instance=parent,initial=initial)
         return render(request,"edit-parents.html",{"form":form,"parent_id":parent_id})
    
     def post(self,request,parent_id):
         user = request.user
         if not user.is_superuser:
             return redirect("dashboard")
         parent = get_object_or_404(CustomUserModel,id=parent_id)
         form = ParentForm(data=request.POST,instance=parent)
         if form.is_valid():
             parent.name = form.cleaned_data.get("name")
             parent.user_phone = form.cleaned_data.get("user_phone")
             parent.email = form.cleaned_data.get("email")
             form.save()
             return redirect("edit-parents", parent_id=parent_id)
         else:
             return render(request,"edit-parents.html",{"form":form,"parent_id":parent_id})
        
class GetParentView(LoginRequiredMixin,View):
     login_url = ""
     redirect_field_name = "next"
     def get(self,request,parent_id=None):
         user = request.user
         if not user.is_superuser:
             return redirect("dashboard")
         if parent_id:
             parent = get_object_or_404(CustomUserModel,id=parent_id)
             return render(request,"view-parents-details.html",{"parent":parent})
         else:
             the_page = request.GET.get("page")
             search_query = request.GET.get("search_query")
             parents = CustomUserModel.objects.all().order_by("name")
             paginator = Paginator(parents, 20)
             if search_query:
                 parents = parents.filter(name__icontains=search_query)
             page = paginator.get_page(the_page)
             return render(request,"view-parents.html",{"parents":page})
        

class DeleteParentView(LoginRequiredMixin,View):
     login_url = "/login/"
     redirect_field_name = "next"
     def post(self,request,parent_id):
         user = request.user
         if not user.is_superuser:
             return redirect("dashboard")
         parent = get_object_or_404(CustomUserModel,id=parent_id)
         parent.delete()
         return redirect("view-parents")
