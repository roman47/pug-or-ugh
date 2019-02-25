from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django.http import Http404
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework import permissions
from rest_framework.request import clone_request
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView
,RetrieveUpdateDestroyAPIView, ListCreateAPIView)
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from . import models
from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class UserPreferences(mixins.CreateModelMixin, RetrieveUpdateAPIView):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer
    lookup_field = 'user'

    def get_object(self):
        queryset = self.get_queryset()
        #import pdb;
        #pdb.set_trace()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            #import pdb;
            #pdb.set_trace()
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        self.perform_update(serializer)
        return Response(serializer.data)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise

class UndecidedNext(APIView):
    def get(self, request, pk, *args, **kwargs):
        # if there are no undecided dogs, return a 404
        dogs = models.Dog.objects.exclude(userdog__status__in='l,d')
        if not dogs:
            return HttpResponseNotFound('<h1>No Page Here</h1>')
        dogs = models.Dog.objects.exclude(userdog__status__in='l,d')\
            .filter(id__gt=pk).first()
        #loop back to the beginning if you hit the last dog
        if not dogs:
            dogs = models.Dog.objects.exclude(userdog__status__in='l,d') \
                .first()
        serializer = serializers.DogSerializer(dogs)
        #import pdb;
        #pdb.set_trace()
        return Response(serializer.data)


class LikedNext(APIView):
    def get(self, request, pk, *args, **kwargs):
        # import pdb;
        # pdb.set_trace()
        # if there are no liked dogs, return a 404
        dogs = models.Dog.objects.filter(userdog__status__in='l')
        if not dogs:
            return HttpResponseNotFound('<h1>No Page Here</h1>')
        dogs = models.Dog.objects.filter(userdog__status__in='l')\
            .filter(id__gt=pk).first()
        # loop back to the beginning if you hit the last dog
        if not dogs:
            dogs = models.Dog.objects.filter(userdog__status__in='l') \
                .first()
        serializer = serializers.DogSerializer(dogs)
        return Response(serializer.data)


class DislikedNext(ListCreateAPIView):
    def get(self, request, pk, *args, **kwargs):
        # if there are no disliked dogs, return a 404
        dogs = models.Dog.objects.filter(userdog__status__in='d')
        if not dogs:
            return HttpResponseNotFound('<h1>No Page Here</h1>')
        dogs = models.Dog.objects.filter(userdog__status__in='d')\
            .filter(id__gt=pk).first()
        # loop back to the beginning if you hit the last dog
        if not dogs:
            dogs = models.Dog.objects.filter(userdog__status__in='d') \
                .first()
        serializer = serializers.DogSerializer(dogs)
        #import pdb;
        #pdb.set_trace()
        return Response(serializer.data)



class Liked(mixins.CreateModelMixin, RetrieveUpdateAPIView):
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.UserDogSerializer

    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        # import pdb;
        # pdb.set_trace()
        serializer = self.get_serializer(instance,
                                         data={"user": request.user.id
                                             , "status": 'l'
                                             , "dog": pk},
                                         partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        self.perform_update(serializer)
        return Response(serializer.data)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise


class Disliked(mixins.CreateModelMixin, RetrieveUpdateAPIView):
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.UserDogSerializer

    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        #import pdb;
        #pdb.set_trace()
        serializer = self.get_serializer(instance,
                                         data={"user": request.user.id
                                                , "status": 'd'
                                                , "dog": pk},
                                         partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        self.perform_update(serializer)
        return Response(serializer.data)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise


class Undecided(mixins.CreateModelMixin, RetrieveUpdateAPIView):
    queryset = models.UserDog.objects.all()
    serializer_class = serializers.UserDogSerializer

    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        # import pdb;
        # pdb.set_trace()
        serializer = self.get_serializer(instance,
                                         data={"user": request.user.id
                                             , "status": 'X'
                                             , "dog": pk},
                                         partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        self.perform_update(serializer)
        return Response(serializer.data)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise


