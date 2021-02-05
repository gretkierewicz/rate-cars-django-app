from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from cars.models import Cars, CarModels, CarRates
from utils.nhtsa_requests import CarsModelsForMake


CARS_PARENT_KWARGS = {'car_make': 'car_make__make'}


class CarRateSerializer(NestedHyperlinkedModelSerializer):
    class Meta:
        model = CarRates
        fields = ['rate']
        extra_kwargs = {
            'rate': {'min_value': 1, 'max_value': 5, }
        }
    parent_lookup_kwargs = CARS_PARENT_KWARGS

    def create(self, validated_data):
        # add model instance - see updating data in Car Model view's action: 'rate'
        car_model = self.initial_data.get('car_model')
        if car_model:
            validated_data.update({'car_model': car_model})
        return super().create(validated_data)


class CarModelsSerializer(NestedHyperlinkedModelSerializer):
    class Meta:
        model = CarModels
        fields = ['url', 'name', 'avg_rate']
        extra_kwargs = {
            'url': {'view_name': 'car-models-detail', 'lookup_field': 'name'},
        }
    parent_lookup_kwargs = CARS_PARENT_KWARGS


class CarsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Cars
        fields = ['url', 'make', 'models',
                  # write-only
                  'model_name']
        extra_kwargs = {
            'url': {'lookup_field': 'make'},
            # disabling unique validator to pass validation process to the .validate() method
            'make': {'validators': []},
        }

    models = CarModelsSerializer(read_only=True, many=True)

    model_name = CharField(write_only=True)

    def validate(self, attrs):
        car_make = attrs.get('make')
        model_name = attrs.pop('model_name')
        # get maker name and models list from vpic.nhtsa.dot.gov/api/
        cars = CarsModelsForMake(car_make)
        if not cars.make_name:
            raise ValidationError(f"No car maker found for {car_make}")
        if not cars.models:
            raise ValidationError(f"No models found for {cars.make_name}")
        try:
            # lowering all model's names to make entering name a bit easier
            fixed_model_name = next(_ for _ in cars.models if _.lower() == model_name.lower())
        except StopIteration:
            # TODO: returning list of possible model's names in compare to provided string
            raise ValidationError(f"No model named {model_name} found in {cars.make_name}'s models")
        # at this point there is car make found (cars.make_name) and model name as well (fixed_model_name)
        # manually check unique together condition to eventually raise error from that method
        try:
            make = Cars.objects.get(make=cars.make_name)
            model = CarModels.objects.get(car_make=make, name=fixed_model_name)
            if model:
                raise ValidationError(
                    {'non_field_errors': ['This make and model combination already exists in database.']})
        except ObjectDoesNotExist:
            # update attrs with fixed data
            attrs.update({'make': cars.make_name, 'model': fixed_model_name})
        return attrs

    def create(self, validated_data):
        model_data = {'name': validated_data.pop('model')}
        car_make, created = Cars.objects.get_or_create(**validated_data)
        model_data.update({'car_make': car_make})
        CarModels.objects.create(**model_data)
        return car_make
