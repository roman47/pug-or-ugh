from django.contrib.auth import get_user_model
from rest_framework import mixins
from django.http import Http404
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework import permissions
from rest_framework.request import clone_request
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView
, ListCreateAPIView)

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
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        self.perform_update(serializer)
        #import pdb;
        #pdb.set_trace()
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


def get_age_range(user_pref_age):
    b_lower_age_limit = 1000
    y_lower_age_limit = 1000
    a_lower_age_limit = 1000
    s_lower_age_limit = 1000
    b_upper_age_limit = 0
    y_upper_age_limit = 0
    a_upper_age_limit = 0
    s_upper_age_limit = 0
    if 'b' in user_pref_age:
        b_lower_age_limit = 0
        b_upper_age_limit = 10
    if 'y' in user_pref_age:
        y_lower_age_limit = 11
        y_upper_age_limit = 20
    if 'a' in user_pref_age:
        a_lower_age_limit = 21
        a_upper_age_limit = 40
    if 's' in user_pref_age:
        s_lower_age_limit = 41
        s_upper_age_limit = 1000

    return (min(b_lower_age_limit, y_lower_age_limit,
                a_lower_age_limit, s_lower_age_limit), max(
                b_upper_age_limit, y_upper_age_limit, a_upper_age_limit,
                s_upper_age_limit))

class UndecidedNext(APIView):
    def get(self, request, pk, *args, **kwargs):
        # get userPrefs
        #import pdb;
        #pdb.set_trace()
        userPref = models.UserPref.objects.get(user__id=request.user.id)
        # get all the dogs based on UserPref
        dogsAll = models.Dog.objects.exclude(userdog__status__in=('l','d'))\
            .filter(gender__in=userPref.gender)\
            .filter(size__in=userPref.size)\
            .filter(age__range=get_age_range(userPref.age))
        # if there are no undecided dogs, return a 404
        if not dogsAll:
            return HttpResponseNotFound('<h1>No Page Here</h1>')
        dogs = dogsAll.filter(id__gt=pk).first()
        #loop back to the beginning if you hit the last dog
        if not dogs:
            dogs = dogsAll.first()
        serializer = serializers.DogSerializer(dogs)
        return Response(serializer.data)

class LikedNext(APIView):
    def get(self, request, pk, *args, **kwargs):
        # get userPrefs
        userPref = models.UserPref.objects.get(user__id=request.user.id)
        # get all the dogs based on UserPref
        dogsAll = models.Dog.objects.filter(userdog__status__in='l')\
            .filter(gender__in=userPref.gender)\
            .filter(size__in=userPref.size)\
            .filter(age__range=get_age_range(userPref.age))
        # import pdb;
        # pdb.set_trace()
        # if there are no undecided dogs, return a 404
        if not dogsAll:
            return HttpResponseNotFound('<h1>No Page Here</h1>')
        dogs = dogsAll.filter(id__gt=pk).first()
        # loop back to the beginning if you hit the last dog
        if not dogs:
            dogs = dogsAll.first()
        serializer = serializers.DogSerializer(dogs)
        return Response(serializer.data)


class DislikedNext(ListCreateAPIView):
    def get(self, request, pk, *args, **kwargs):
        # get userPrefs
        userPref = models.UserPref.objects.get(user__id=request.user.id)
        # get all the dogs based on UserPref
        dogsAll = models.Dog.objects.filter(userdog__status__in='d')\
            .filter(gender__in=userPref.gender)\
            .filter(size__in=userPref.size)\
            .filter(age__range=get_age_range(userPref.age))
        # import pdb;
        # pdb.set_trace()
        # if there are no undecided dogs, return a 404
        if not dogsAll:
            return HttpResponseNotFound('<h1>No Page Here</h1>')
        dogs = dogsAll.filter(id__gt=pk).first()
        # loop back to the beginning if you hit the last dog
        if not dogs:
            dogs = dogsAll.first()
        serializer = serializers.DogSerializer(dogs)
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


