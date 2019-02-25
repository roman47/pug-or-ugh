from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from . import models
from . import serializers
import json
from os import environ
from os import path
import sys

from rest_framework.test import force_authenticate
from .views import (UserRegisterView, UserPreferences, LikedNext,
                            DislikedNext, UndecidedNext, Liked, Disliked,
                            Undecided)


class PugOrUghTests(APITestCase):
    def setUp(self):
        PROJ_DIR = path.dirname(path.dirname(path.abspath(__file__)))
        filepath = path.join(PROJ_DIR, 'pugorugh', 'static',
                             'dog_details.json')
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

            serializer = serializers.DogSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

        self.user = User.objects.create_superuser('adminTest',
                                                  'admin@admin.com',
                                                  'admin123')
        self.factory = APIRequestFactory()
        self.user = User.objects.get(username='adminTest')

    def test_liked(self):
        """
        Test liked
        """
        view = Liked.as_view()
        url = reverse('liked', kwargs={'pk': 2})
        data = {}
        request = self.factory.put(url, data=data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=2)
        response.render()
        #import pdb;
        #pdb.set_trace()
        self.assertEqual(response.status_code, 201)

        view = LikedNext.as_view()
        url = reverse('liked-next', kwargs={'pk': 2})
        data = {}
        request = self.factory.get(url, data=data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=2)
        response.render()
        # import pdb;
        # pdb.set_trace()
        self.assertEqual(response.status_code, 200)

    def test_disliked(self):
        """
        Test disliked
        """
        view = Disliked.as_view()
        url = reverse('disliked', kwargs={'pk': 3})
        data = {}
        request = self.factory.put(url, data=data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=3)
        response.render()
        # import pdb;
        # pdb.set_trace()
        self.assertEqual(response.status_code, 201)

        view = DislikedNext.as_view()
        url = reverse('disliked-next', kwargs={'pk': 3})
        data = {}
        request = self.factory.get(url, data=data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=3)
        response.render()
        # import pdb;
        # pdb.set_trace()
        self.assertEqual(response.status_code, 200)

    def test_undecided(self):
        """
        Test undecided
        """
        view = Undecided.as_view()
        url = reverse('undecided', kwargs={'pk': 1})
        data = {}
        request = self.factory.put(url, data=data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        response.render()
        # import pdb;
        # pdb.set_trace()
        self.assertEqual(response.status_code, 201)


    def test_undecided_next(self):
        """
        Test undecided next
        """
        view = UndecidedNext.as_view()
        url = reverse('undecided-next', kwargs={'pk': 1})
        data = {}
        request = self.factory.get(url, data=data, format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        response.render()
        # import pdb;
        # pdb.set_trace()
        self.assertEqual(response.status_code, 200)
