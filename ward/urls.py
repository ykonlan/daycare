from django.urls import path,include
from . import views

urlpatterns = [
    path("add/",views.WardView.as_view(),name="add-ward"),
    path("view/<int:ward_id>",views.WardView.as_view(),name="view-ward-details"),
]