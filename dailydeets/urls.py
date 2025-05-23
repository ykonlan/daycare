from django.urls import path
from . import views

urlpatterns = [
    path("fill/",views.FillDailyDeetForm.as_view(),name="fill-forms"),
    
]