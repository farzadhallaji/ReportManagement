from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.sign_in, name='home'),  # Set the sign-in page as the homepage

    path('create/', views.create_report, name='create_report'),
    path('edit/<int:report_id>/', views.edit_report, name='edit_report'),
    path('create_account/', views.create_account, name='create_account'),
    path('delete/<int:report_id>/', views.delete_report, name='delete_report'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),

]

