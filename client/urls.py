from django.urls import path

from . import views

urlpatterns = [
    path('', views.ClientListView.as_view(),name='clients_list'),
    path('<int:pk>/',views.ClientDetailView.as_view(),name='clients_detail'),
    path('<int:pk>/delete/',views.ClientDeleteView.as_view(),name='clients_delete'),
    path('<int:pk>/edit/',views.clients_edit,name='clients_edit'),
    path('<int:pk>/add-file/',views.AddFileView.as_view(),name='add_file'),
    path('<int:pk>/add-comment/',views.AddCommentView2.as_view(),name='add_comment'),
    path('add/',views.clients_add,name='clients_add'),
    path('export/',views.clients_export, name='export'),
]