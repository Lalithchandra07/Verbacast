from django.urls import include, path
from . import views
from django.conf.urls.i18n import set_language
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('translated_video/', views.translate_video_view, name='translate_video'),
    path('login/',views.user_login,name='login'),
    path('register/',views.user_register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),
    # path('set-language/', set_language, name='set_language'),
    path('i18n/', include('django.conf.urls.i18n')),
]

