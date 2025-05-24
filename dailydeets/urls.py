from django.urls import path
from . import views

urlpatterns = [
    path("fill/",views.WardSelect.as_view(),name="fill-forms"),
    path("upload/<int:ward_id>/",views.FillDailyDeetForm.as_view(),name="upload-forms"),
    
]