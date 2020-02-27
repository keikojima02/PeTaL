from django.urls import path
from _main.views import PetalHomeView

urlpatterns = [
    path('', PetalHomeView.as_view(), name='petalhome'),
]
