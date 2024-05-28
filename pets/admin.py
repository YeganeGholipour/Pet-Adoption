from django.contrib import admin
from .models import User, Animal, Location, Adoption

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'address', 'role', 'birth_date', 'join_date', 'role']

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['status', 'species', 'breed', 'gender', 'name', 'age', 'location']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['address', 'name', 'phone_number']

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ['adopter', 'animal', 'adoption_date']
