from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework_nested.viewsets import NestedViewSetMixin

from cars.models import Cars, CarModels
from cars.serializers import CarsSerializer, CarModelsSerializer, CarRateSerializer, PopularCarsSerializer


class CarMakesViewSet(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    lookup_field = 'make'

    @action(detail=False, methods=['GET'])
    # display 5 most rated car models
    def popular(self, request, *args, **kwargs):
        # swap to Popular Cars Serializer in case of this action
        self.serializer_class = PopularCarsSerializer
        queryset = CarModels.objects.annotate(count=Count('rates__id')).order_by('-count', 'car_make', 'name')[:5]
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class CarModelsViewSet(NestedViewSetMixin,
                       # Nested View Set Mixin auto filters queryset with serializer's parent lookup kwargs
                       GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin):

    queryset = CarModels.objects.all()
    serializer_class = CarModelsSerializer
    lookup_field = 'name'

    @action(detail=True, methods=['GET', 'POST'])
    # post rate for specific car make and model
    def rate(self, request, *args, **kwargs):
        # swap to Car Rate Serializer in case of this action
        self.serializer_class = CarRateSerializer
        if request.method == 'POST':
            data = request.data.copy()
            # update data with car_model instance so it can be serialized easily
            data.update({'car_model': self.get_object()})
            rate_serializer = self.get_serializer(data=data)
            if rate_serializer.is_valid():
                # validate and save rate
                rate_serializer.save()
            return Response(
                rate_serializer.errors or rate_serializer.data,
                status=status.HTTP_400_BAD_REQUEST if rate_serializer.errors else status.HTTP_200_OK)
        # GET method -  get_object() to throw error for wrong url / object not found
        self.get_object()
        return Response(None)
