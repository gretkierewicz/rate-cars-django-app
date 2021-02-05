from rest_framework.viewsets import GenericViewSet, mixins

from cars.models import Cars, CarModels
from cars.serializers import CarsSerializer, CarModelsSerializer


class CarMakesViewSet(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    lookup_field = 'make'


class CarModelsViewSet(GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin):
    queryset = CarModels.objects.all()
    serializer_class = CarModelsSerializer
    lookup_field = 'name'
