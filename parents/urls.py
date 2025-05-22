from django.urls import path
from . import views

urlpatterns = [
    path("add/",views.AddParentView.as_view(),name="add-parent"),
    path("view/<int:parent_id>",views.GetParentView.as_view(),name="view-parent-details"),
    path("view/",views.GetParentView.as_view(),name="view-parents"),
    path("edit/<int:parent_id>",views.EditParentView.as_view(),name="edit-parents"),
    path("delete/<int:parent_id>",views.DeleteParentView.as_view(),name="delete-parent")
]