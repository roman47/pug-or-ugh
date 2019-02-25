from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from .views import (UserRegisterView, UserPreferences, LikedNext,
                            DislikedNext, UndecidedNext, Liked, Disliked,
                            Undecided)

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/dog/(?P<pk>-?\d+)/liked/next/$', LikedNext.as_view(),
        name='liked-next'),
    url(r'^api/dog/(?P<pk>-?\d+)/disliked/next/$', DislikedNext.as_view(),
        name='disliked-next'),
    url(r'^api/dog/(?P<pk>-?\d+)/undecided/next/$', UndecidedNext.as_view(),
        name='undecided-next'),
    url(r'^api/dog/(?P<pk>\d+)/liked/$', Liked.as_view(),
        name='liked'),
    url(r'^api/dog/(?P<pk>\d+)/disliked/$', Disliked.as_view(),
        name='disliked'),
    url(r'^api/dog/(?P<pk>\d+)/undecided/$', Undecided.as_view(),
        name='undecided'),
    url(r'^api/user/preferences/$', UserPreferences.as_view(), name='user-preferences'),
])
