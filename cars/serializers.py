from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from cars.models import Cars, CarModels


class CarModelsSerializer(NestedHyperlinkedModelSerializer):
    class Meta:
        model = CarModels
        fields = ['url', 'name']
        extra_kwargs = {
            'url': {'view_name': 'car-models-detail', 'lookup_field': 'name'},
        }
    parent_lookup_kwargs = {
        'car_make': 'car_make__make'
    }


class CarsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Cars
        fields = ['make', 'models']

    models = CarModelsSerializer(read_only=True, many=True)
