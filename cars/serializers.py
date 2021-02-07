from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
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

    parent_lookup_kwargs = CARS_PARENT_KWARGS

    url = NestedHyperlinkedIdentityField(
        view_name='car-models-detail',
        lookup_field='name',
        # lookup_url_kwarg same as lookup_field, no need to set up
        parent_lookup_kwargs=parent_lookup_kwargs
    )


class PopularCarsSerializer(CarModelsSerializer):
    class Meta:
        model = CarModels
        fields = ['url', 'car_make', 'name', 'rates_number', 'avg_rate']

    car_make = SlugRelatedField(read_only=True, slug_field='make')


class CarsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Cars
        fields = ['url', 'make', 'models']
        extra_kwargs = {
            'url': {'lookup_field': 'make'},
        }

    models = CarModelsSerializer(many=True)

    def validate(self, attrs):
        # get car make's name and models list from vpic.nhtsa.dot.gov/api/
        cars = CarsModelsForMake(attrs.get('make'))
        if not cars.make_name:
            raise ValidationError(f"No car maker found for {attrs.get('make')}")
        attrs.update({'make': cars.make_name})
        if not cars.models:
            raise ValidationError(f"No models found for {cars.make_name}")
        try:
            for model in attrs.get('models'):
                # lowering all model's names to make entering name a bit easier
                fixed_model_name = next(_ for _ in cars.models if _.lower() == model['name'].lower())
                model.update({'name': fixed_model_name})
        except StopIteration:
            # TODO: returning list of possible model's names in compare to provided string
            raise ValidationError(f"No model named {model['name']} found in {cars.make_name}'s models")
        # at this point there is car make found (cars.make_name) and model names as well
        return attrs

    def create(self, validated_data):
        models = validated_data.pop('models')
        car_make, created = Cars.objects.get_or_create(**validated_data)
        # creating car make's models as well
        for model in models:
            # get_or_create() to avoid unique_together validation error
            car_make.models.get_or_create(**model)
        return car_make
