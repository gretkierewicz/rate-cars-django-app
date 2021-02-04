from rest_framework.viewsets import ModelViewSet

from cars.models import Cars
from cars.serializers import CarsSerializer


class CarsViewSet(ModelViewSet):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
