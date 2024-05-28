from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from .models import Animal, User, Adoption, Location, AdoptionStatusChoices, UserRolesChoices
from .serializers import AnimalSerializer, UserSerializer, AdoptionSerializer, LocationSerializer, TokenLoginSerializer, RegisterationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from pets import serializers

class ListAllAnimals(ListAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    # permission_classes = []

class ListAllNotAdoptedAnimals(ListAPIView):
    queryset = Animal.objects.filter(status=AdoptionStatusChoices.NOTADOPTED)
    serializer_class = AnimalSerializer
    # permission_classes = []

class RetrieveAnAnimal(RetrieveAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    # permission_classes = []

class RegisterAnAnimal(CreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    # permission_classes = []

class AssignAdoption(APIView):

    def get(self, request, *args, **kwargs):
        # Provide the lists of all users and non-adopted animals
        users = User.objects.all()
        animals = Animal.objects.filter(status=AdoptionStatusChoices.NOTADOPTED)
        
        users_data = [{"id": user.id, "username": user.username} for user in users]
        animals_data = [{"id": animal.id, "name": animal.name} for animal in animals]
        
        return Response({
            "users": users_data,
            "animals": animals_data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = AdoptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterAnAdopter(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = []

class ListAllAdopters(ListAPIView):
    queryset = User.objects.filter(role=UserRolesChoices.ADOPTER)
    serializer_class = UserSerializer
    # permission_classes = []

class ListAllAdoptions(ListAPIView):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
    # permission_classes = []

class ListAllLocations(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # permission_classes = []

class RetrieveAnAdoption(RetrieveAPIView):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
    # permission_classes = []

# class UpdateAdoptionStatusView(UpdateAPIView):
#     queryset = Animal.objects.all()
#     serializer_class = UpdateAdoptionStatusSerializer
#     # permission_classes = []

class RegisterUser(APIView):
    # permission_classes = []
    serializer_class = RegisterationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(status=status.HTTP_201_CREATED)
        

class TokenLoginView(APIView):
    # permission_classes = []
    serializer_class = TokenLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class TokenLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            Token.objects.get(user=request.user).delete()
        except Token.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
