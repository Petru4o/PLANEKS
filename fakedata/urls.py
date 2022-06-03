from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainList.as_view(), name='home'),

    path('login/', views.LoginV.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('create_schema/', views.SchemaCreateView.as_view(), name='create_schema'),
    path('delete_schema/<int:pk>/', views.DeleteSchemaView.as_view(), name='delete_schema' ),

    path('schema/<int:pk>/', views.DataSetView.as_view(), name='schema_dataset'),

]
