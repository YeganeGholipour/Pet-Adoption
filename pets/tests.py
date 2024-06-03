from rest_framework.test import APIClient
from django.urls import reverse
from .models import User, Location, Animal, Adoption, UserRolesChoices
from rest_framework import status
from django.test import TestCase
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)

class AnimalTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
    
    def test_list_animals(self):
        location = Location.objects.create(
            address="123 Main St",
            name="Alex",
            phone_number="123-456-7890"
        )

        animal = Animal.objects.create(
            status='A',
            species="dog",
            breed="German Shepherd",
            gender="M",
            name="Max",
            age=5,
            location=location
        )

        response = self.client.get(reverse('list-animals'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) != 0)

    def test_register_an_animal(self):
        location = {
            "address":"124 Main St",
            "name": "Yegane",
            "phone_number": "122-456-7890"
        }

        animal_data = {
            'status': 'A',
            'species': "cat",
            'breed': "Siamese",
            'gender': "M",
            'name': "Whiskers",
            'age': 2,
            'location': location
        }

        response = self.client.post(reverse('register-an-animal'), animal_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(len(response.data) != 0)

    def test_list_not_adopted_animals(self):
        location = Location.objects.create(
            address="123 Star St",
            name="Andi",
            phone_number="123-456-7890"
        )

        animal = Animal.objects.create(
            status='N',
            species="dog",
            breed="Golden Retriever",
            gender="M",
            name="Buddy",
            age=5,
            location=location
        )

        response = self.client.get(reverse('list-not-adopted-animals'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) != 0)

    def test_retrieve_an_animal(self):
        location = Location.objects.create(
            address="123 Comm St",
            name="Presi",
            phone_number="123-458-7890"
        )

        animal = Animal.objects.create(
            status='A',
            species="dog",
            breed="German Shepherd",
            gender="F",
            name="Max",
            age=3,
            location=location
        )

        response = self.client.get(reverse('retrieve-an-animal', kwargs={'pk': animal.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) != 0)

    def test_list_adopters(self):
        user = User.objects.create(
            username="Alex",
            email="alex@alex",
            password="alex123",
            role=UserRolesChoices.ADOPTER,
            phone_number="123-456-7890",
            address="123 Comm St",
            birth_date="2000-01-01"
        )

        response = self.client.get(reverse('list-adopters'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) != 0)

    def test_list_adoption(self):
        location = Location.objects.create(
            address="123 Star St",
            name="Andi",
            phone_number="123-456-7890"
        )

        animal = Animal.objects.create(
            status='A',
            species="dog",
            breed="Golden Retriever",
            gender="M",
            name="Buddy",
            age=5,
            location=location
        )

        user = User.objects.create(
            username="Alex",
            email="alex@alex",
            password="alex123",
            role=UserRolesChoices.ADOPTER,
            phone_number="123-456-7890",
            address="123 Comm St",
            birth_date="2000-01-01"
        )

        adoption = Adoption.objects.create(
            animal=animal,
            adopter=user
        )

        response = self.client.get(reverse('list-adoptions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) != 0)

    def test_list_locations(self):
        location = Location.objects.create(
            address="128 Comm St",
            name="Naser",
            phone_number="129-456-7890"
        )

        response = self.client.get(reverse('list-locations'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) != 0)

    def test_retrieve_an_adoption(self):
        location = Location.objects.create(
            address="123 Star St",
            name="Andi",
            phone_number="123-456-7890"
        )

        animal = Animal.objects.create(
            status='A',
            species="dog",
            breed="Golden Retriever",
            gender="M",
            name="Buddy",
            age=5,
            location=location
        )

        user = User.objects.create(
            username="Alex",
            email="alex@alex",
            password="alex123",
            role=UserRolesChoices.ADOPTER,
            phone_number="123-456-7890",
            address="123 Comm St",
            birth_date="2000-01-01"
        )

        adoption = Adoption.objects.create(
            animal=animal,
            adopter=user
        )

        response = self.client.get(reverse('retrieve-an-adoption', kwargs={'pk': adoption.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) != 0)

    def test_update_user(self):
        user = User.objects.create(
            username="Alex",
            email="alex@alex",
            password="alex123",
            role=UserRolesChoices.ADOPTER,
            phone_number="123-456-7890",
            address="123 Comm St",
            birth_date="2000-01-01"
        )

        updated_data = {
            'address': "123 new new new new St"
        }

        response = self.client.patch(reverse('update-user', kwargs={'pk': user.pk}), updated_data)
    

    def test_update_animal(self):
        location = {
            'address': "123 Comm St",
            'name': "fatiii",
            'phone_number': "123-458-7890"
        }

        location = Location.objects.create(**location)
        animal = Animal.objects.create(
            status='N',
            species="cat",
            breed="Golden Retriever",
            gender="F",
            name="Buddy",
            age=5,
            location=location
        )
        pk = animal.id

        updated_data = {
            'age': 23
        }

        response = self.client.patch(reverse('update-animal', kwargs={'pk': pk}), updated_data)

    



# class UserTest(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.register_url = reverse('register-user')
#         self.login_url = reverse('token-login')
#         self.logout_url = reverse('token-logout')

#         self.user_data = {
#             'username': "Monir",
#             'email': "monir@monir",
#             'password': "alex123",
#             'role': UserRolesChoices.ADOPTER,
#             'phone_number': "123-456-7890",
#             'address': "123 Comm St",
#             'birth_date': "2000-01-01"
#         }

#         self.login_data = {
#             'username': "Monir",
#             'password': "alex123",
#         }


#     def test_register_user(self):
#         response = self.client.post(self.register_url, self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(User.objects.filter(username="Monir").exists())


#     def test_login_user(self):
#         self.client.post(self.register_url, self.user_data)
#         response = self.client.post(self.login_url, self.login_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(Token.objects.filter(user__username="Monir").exists())

    
#     def test_logout_user(self):
#         self.client.post(self.register_url, self.user_data)
#         self.client.post(self.login_url, self.login_data, format='json')
#         response = self.client.post(self.logout_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Token.objects.filter(user__username="Monir").exists())