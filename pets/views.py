from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Animal, Adopter, Adoption, Location, AdoptionStatusChoices
from .serializers import  AnimalSerializer, AdopterSerializer, AdoptionSerializer, LocationSerializer, UpdateAdoptionStatusSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class ListAllAnimals(ListAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = []


class ListAllNotAdoptedAnimals(ListAPIView):
    queryset = Animal.objects.filter(status=AdoptionStatusChoices.NOTADOPTED)
    serializer_class = AnimalSerializer
    permission_classes = []


class RetrieveAnAnimal(RetrieveAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = []

class RegisterAnAnimal(CreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = []


class AssignAdoption(CreateAPIView):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
    permission_classes = []

class RegisterAnAdopter(CreateAPIView):
    queryset = Adopter.objects.all()
    serializer_class = AdopterSerializer
    permission_classes = []


class ListAllAdopters(ListAPIView):
    queryset = Adopter.objects.all()
    serializer_class = AdopterSerializer
    permission_classes = []

class ListAllAdoptions(ListAPIView):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
    permission_classes = []

class ListAllLocations(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = []

class RetrieveAnAdoption(RetrieveAPIView):
    queryset = Adoption.objects.all()
    serializer_class = UpdateAdoptionStatusSerializer
    permission_classes = []


# class register(APIView):
#     permission_classes = []
#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = 

# login