from rest_framework import serializers

from .models import Evants


class EvantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evants
        fields = "__all__"
