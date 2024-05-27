from rest_framework import serializers
from .models import Animal, Location, Adopter, Adoption, AdoptionStatusChoices

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AdopterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopter
        fields = ['name', 'phone_number', 'address', 'birth_date', 'join_date']


class AnimalSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    
    class Meta:
        model = Animal
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location, created = Location.objects.get_or_create(**location_data)
        animal = Animal.objects.create(location=location, **validated_data)
        return animal

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location')
        location, created = Location.objects.get_or_create(**location_data)
        
        instance.status = validated_data.get('status', instance.status)
        instance.species = validated_data.get('species', instance.species)
        instance.breed = validated_data.get('breed', instance.breed)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.location = location
        instance.save()
        
        return instance


class AdoptionSerializer(serializers.ModelSerializer):
    animal = AnimalSerializer()
    adopter = AdopterSerializer()

    class Meta:
        model = Adoption
        fields = '__all__'

    def create(self, validated_data):
        animal_data = validated_data.pop('animal')
        adopter_data = validated_data.pop('adopter')

        animal, created = Animal.objects.get_or_create(**animal_data)
        adopter, created = Adopter.objects.get_or_create(**adopter_data)

        adoption = Adoption.objects.create(animal=animal, adopter=adopter, status=AdoptionStatusChoices.ADOPTED, **validated_data)
        return adoption

    def update(self, instance, validated_data):
        animal_data = validated_data.pop('animal')
        adopter_data = validated_data.pop('adopter')

        animal, created = Animal.objects.get_or_create(**animal_data)
        adopter, created = Adopter.objects.get_or_create(**adopter_data)

        instance.animal = animal
        instance.adopter = adopter
        instance.adoption_date = validated_data.get('adoption_date', instance.adoption_date)
        
        instance.save()
        
        return instance

class UpdateAdoptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['status']

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        
        if status == AdoptionStatusChoices.NOTADOPTED:
            # Delete the corresponding adoption record if it exists
            Adoption.objects.filter(animal=instance).delete()
        
        instance.status = status
        instance.save()
        
        return instance