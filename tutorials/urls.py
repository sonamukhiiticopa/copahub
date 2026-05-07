from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('tutorial/<slug:subject_slug>/<slug:topic_slug>/', views.tutorial_detail, name='tutorial_detail'),
]