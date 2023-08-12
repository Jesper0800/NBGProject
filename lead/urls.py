from django.urls import path

from . import views

urlpatterns = [
    path('',views.leads_list, name='leads_list'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
    path('<int:pk>/delete/', views.leads_delete, name='leads_delete'),
    path('<int:pk>/edit/', views.leads_edit, name='leads_edit'),
    path('<int:pk>/add-comment2/',views.AddCommentView.as_view(),name='add_comment2'),
    path('<int:pk>/convert/', views.convert_to_client, name='leads_convert'),
    path('add-lead/', views.add_lead, name='add_lead'),
]