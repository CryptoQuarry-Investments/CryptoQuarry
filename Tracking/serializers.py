from rest_framework import serializers

from .models import AlgorithmUtilisation

class AlgorithmUtilisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AlgorithmUtilisation
        fields = (
            'algorithm_name',
            'count'
        )
