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
        fields = ['username', 'email', 'phone_number', 'address', 'birth_date', 'join_date']
        
        

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
    animal = serializers.StringRelatedField()
    adopter = serializers.StringRelatedField()

    class Meta:
        model = Adoption
        fields = '__all__'

    def create(self, validated_data):
        animal_name = validated_data.pop('animal')
        adopter_username = validated_data.pop('adopter')

        # Fetch the animal instance using name
        animal = Animal.objects.get(name=animal_name)
        animal.status = AdoptionStatusChoices.ADOPTED
        animal.save()

        # Fetch the adopter instance using username
        adopter = User.objects.get(username=adopter_username)
        adopter.role = UserRolesChoices.ADOPTER
        adopter.save()

        # Create the adoption record
        adoption = Adoption.objects.create(animal=animal, adopter=adopter, **validated_data)

        return adoption

    def update(self, instance, validated_data):
        animal_name = validated_data.pop('animal')
        adopter_username = validated_data.pop('adopter')

        # Fetch and update the animal instance using name
        animal = Animal.objects.get(name=animal_name)
        animal.status = AdoptionStatusChoices.ADOPTED
        animal.save()

        # Fetch and update the adopter instance using username
        adopter = User.objects.get(username=adopter_username)
        adopter.role = UserRolesChoices.ADOPTER
        adopter.save()

        # Update the adoption record
        instance.animal = animal
        instance.adopter = adopter
        instance.adoption_date = validated_data.get('adoption_date', instance.adoption_date)
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
    password = serializers.CharField(max_length=100, write_only=True)
    confirm_password = serializers.CharField(max_length=100, write_only=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'phone_number', 'address', 'birth_date')
        write_only_fields = ['password', 'confirm_password']

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

        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        phone_number = validated_data.get('phone_number', '')
        address = validated_data.get('address', '')
        birth_date = validated_data.get('birth_date', None)

        user = User(
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            birth_date=birth_date,
            role=User.USER_ROLES_CHOICES.USER  
        )
        user.set_password(password)
        user.save()

        return user


