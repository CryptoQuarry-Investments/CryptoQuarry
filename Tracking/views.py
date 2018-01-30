from rest_framework import viewsets

from django.shortcuts import render

from .models import AlgorithmUtilisation
from .serializers import AlgorithmUtilisationSerializer

## API ENDPOINTS

class AlgorithmUtilisationViewSet(viewsets.ModelViewSet):
    queryset = AlgorithmUtilisation.objects.all()
    serializer_class = AlgorithmUtilisationSerializer
