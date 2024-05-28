from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class UserRolesChoices(models.TextChoices):
    ADOPTER = '0', 'Adopter'
    USER = '1', 'User'

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=1, choices=UserRolesChoices.choices, default=UserRolesChoices.USER)

    groups = models.ManyToManyField(
        Group,
        related_name='pets_user_set',  # Change the related_name to avoid clash
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='pets_user_permissions_set',  # Change the related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )


    @property
    def age(self):
        if self.birth_date:
            today = datetime.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    def __str__(self):
        return self.username  

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
    adopter = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': UserRolesChoices.ADOPTER})
    adoption_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.adopter.phone_number} has adopted {self.animal.name}."
