from django.urls import path,include
from . import views

urlpatterns = [
    path("add/",views.AddWardView.as_view(),name="add-ward"),
    path("view/<int:ward_id>",views.GetWardView.as_view(),name="view-ward-details"),
    path("view/",views.GetWardView.as_view(),name="view-wards"),
    path("edit/<int:ward_id>",views.PatchWardView.as_view(),name="edit-wards"),
    path("delete/<int:ward_id>",views.DeleteWardView.as_view(),name="delete-ward")
]