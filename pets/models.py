from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class Adopter(AbstractUser):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)  
    address = models.TextField()
    birth_date = models.DateField()
    join_date = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        today = datetime.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        return self.name

class GenderChoices(models.TextChoices):
    FEMALE = 'F', 'Female'
    MALE = 'M', 'Male'

class AdoptionStatusChoices(models.TextChoices):
    ADOPTED = 'A', 'Adopted'
    NOTADOPTED = 'N', 'Not Adopted'

class Location(models.Model):
    address = models.TextField()
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)  

    def __str__(self):
        return self.name

class Animal(models.Model):
    status = models.CharField(max_length=1, choices=AdoptionStatusChoices.choices)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    name = models.CharField(max_length=100)
    age = models.IntegerField() 
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Adoption(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE)
    adoption_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.adopter.name} has adopted {self.animal.name}."
