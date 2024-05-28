from rest_framework import serializers
from .models import Animal, Location, User, Adoption, AdoptionStatusChoices, UserRolesChoices
from django.contrib.auth import authenticate

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

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
    adopter = UserSerializer()

    class Meta:
        model = Adoption
        fields = '__all__'

    def create(self, validated_data):
        animal_data = validated_data.pop('animal')
        adopter_data = validated_data.pop('adopter')

        animal, created = Animal.objects.get_or_create(status=AdoptionStatusChoices.ADOPTED, **animal_data)
        adopter, created = User.objects.get_or_create(role=UserRolesChoices.ADOPTER, **adopter_data)

        adoption = Adoption.objects.create(animal=animal, adopter=adopter, **validated_data)
        animal.status = AdoptionStatusChoices.ADOPTED
        animal.save()

        return adoption

    def update(self, instance, validated_data):
        animal_data = validated_data.pop('animal')
        adopter_data = validated_data.pop('adopter')

        animal, created = Animal.objects.get_or_create(**animal_data)
        adopter, created = User.objects.get_or_create(**adopter_data)

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

class TokenLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username:
            raise serializers.ValidationError('Username is required')

        if not password:
            raise serializers.ValidationError('Password is required')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        data['user'] = user
        return data

class RegisterationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email')
        write_only_fields = ['username', 'password', 'confirm_password', 'email']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        email = data.get('email')
        username = data.get('username')

        if not username:
            raise serializers.ValidationError('Username is required')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')

        if not email:
            raise serializers.ValidationError('Email is required')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')

        if password and confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError('Passwords do not match')
        else:
            raise serializers.ValidationError('Password is required')

        user = User.objects.create(username=username, email=email)
        data['user'] = user

        return data

