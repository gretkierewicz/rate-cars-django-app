from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework_nested.viewsets import NestedViewSetMixin

from cars.models import Cars, CarModels
from cars.serializers import CarsSerializer, CarModelsSerializer, CarRateSerializer


class CarMakesViewSet(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    lookup_field = 'make'


class CarModelsViewSet(NestedViewSetMixin,
                       # Nested View Set Mixin auto filters queryset with parent kwargs
                       GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin):

    queryset = CarModels.objects.all()
    serializer_class = CarModelsSerializer
    lookup_field = 'name'

    @action(detail=True, methods=['GET', 'POST'])
    def rate(self, request, *args, **kwargs):
        # swap to Car Rate Serializer in case of this action
        self.serializer_class = CarRateSerializer
        data = request.data.copy()
        # update data with car_model instance so it can be serialized easily
        data.update({'car_model': self.get_object()})
        rate_serializer = self.get_serializer(data=data)
        if rate_serializer.is_valid():
            # validate and save rate
            rate_serializer.save()
        return Response(rate_serializer.errors or rate_serializer.data)
