from django.urls import path
from . import views
from .views import GetSpecies, GetArticleTitles

urlpatterns = [
    path('', views.birdhome, name='index'),
    path('results/', views.birdresults, name='bird-results'),

    path('species/', GetSpecies.as_view(), name='bird-results'),
    path('titles/', GetArticleTitles.as_view(), name='bird-results'),
]
