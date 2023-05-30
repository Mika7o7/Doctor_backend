from rest_framework import viewsets

from .models import Evants
from .serializers import EvantsSerializer


class EvantsViewSet(viewsets.ModelViewSet):
    queryset = Evants.objects.all()
    serializer_class = EvantsSerializer
