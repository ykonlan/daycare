from django.urls import path,include
from . import views

urlpatterns = [
    path("add/",views.AddStaffView.as_view(),name="add-staff"),
    path("edit/<int:staff_id>",views.EditStaffView.as_view(),name="edit-staff"),
    path("view/<int:staff_id>",views.GetStaffView.as_view(),name="view-staff-details"),
    path("view/",views.GetStaffView.as_view(),name="view-staff"),
    path("delete/<int:staff_id>",views.DeleteStaffView.as_view(),name="delete-staff"),
]