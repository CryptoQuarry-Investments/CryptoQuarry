from rest_framework import viewsets

from django.shortcuts import render

from .models import Worker, Wallet
from .serializers import WorkerSerializer, WalletSerializer

## API ENDPOINTS

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
