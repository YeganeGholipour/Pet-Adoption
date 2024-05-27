from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('animal/<int:animal_id>/', views.animal_detail, name='animal_detail'),
    path('shelters/', views.shelter_list, name='shelter_list'),
    path('shelter/<int:shelter_id>/', views.shelter_detail, name='shelter_detail'),
]
