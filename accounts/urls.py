from django.contrib import admin
from django.urls import path
from .views import *

app_name='accounts'
urlpatterns = [
    path('signup/client/', client_signup, name='c_s'),
    path('signup/server/', server_signup, name='s_s'),

    path('client/<int:client_id>/', ClientProfile, name='client_profile'),
    path('server/<int:server_id>/', ServerProfile, name='server_profile'),

    path('client/update/<int:pk>/', ClientUpdate.as_view(), name='client_update'),
    path('server/update/<int:pk>/', ServerUpdate.as_view(), name='server_update'),

    path('category/<int:pk>/', CategoryDetail.as_view(), name='c_detail'),

    path('server/all/', AllServers.as_view(), name='all_server'),

    path('server/<int:pk>/add/experience/', AddExperience.as_view(), name='add_exp'),

    path('server/<int:server_id>/add/ratings/', add_rating, name='add_rate'),

    path('server/<int:server_id>/add/contact/', add_request, name='add_request'),
]