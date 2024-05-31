from django.urls import path
from . import views

urlpatterns = [
    path('list_animals/', views.ListAllAnimals.as_view(), name='list-animals'),
    path('list_not_adopted_animals/', views.ListAllNotAdoptedAnimals.as_view(), name='list-not-adopted-animals'),
    path('retrieve_an_animal/<int:pk>/', views.RetrieveAnAnimal.as_view(), name='retrieve-an-animal'),
    path('register_an_animal/', views.RegisterAnAnimal.as_view(), name='register-an-animal'),
    path('assign_adoption/', views.AssignAdoption.as_view(), name='assign-adoption'),
    path('retrieve_an_adoption/<int:pk>/', views.RetrieveAnAdoption.as_view(), name='retrieve-an-adoption'),
    path('list_adopters/', views.ListAllAdopters.as_view(), name='list-adopters'),
    path('list_adoptions/', views.ListAllAdoptions.as_view(), name='list-adoptions'),
    path('list_locations/', views.ListAllLocations.as_view(), name='list-locations'),
    path('update_user/<int:pk>', views.UpdateUser.as_view(), name='update-user'),
    path('token_logout/', views.TokenLogoutView.as_view(), name='token-logout'),
    path('token_login/', views.TokenLoginView.as_view(), name='token-login'),
    path('register_user/', views.RegisterUser.as_view(), name='register-user'),
]
