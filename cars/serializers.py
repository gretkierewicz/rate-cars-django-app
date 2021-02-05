from rest_framework.exceptions import ValidationError
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from cars.models import Cars
from utils.nhtsa_requests import CarsModelsForMake


class CarsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Cars
        fields = '__all__'
        validators = [
            # overriding validator's message
            UniqueTogetherValidator(
                queryset=Cars.objects.all(),
                fields=['car_make', 'model_name'],
                message='This model already exists in database.',
            )
        ]

    def validate(self, attrs):
        # get maker name and models list from vpic.nhtsa.dot.gov/api/
        cars = CarsModelsForMake(attrs.get('car_make'))
        if not cars.make_name:
            raise ValidationError(f"No car maker found for {attrs.get('car_make')}")
        if not cars.models:
            raise ValidationError(f"No models found for {cars.make_name}")
        try:
            # lowering all model's names to make entering name a bit easier
            model_name = next(_ for _ in cars.models if _.lower() == attrs.get('model_name').lower())
        except StopIteration:
            # TODO: returning list of possible model's names in compare to provided string
            raise ValidationError(f"No model named {attrs.get('model_name')} found in {cars.make_name}'s models")
        attrs.update({'car_make': cars.make_name, 'model_name': model_name})
        # as .run_validators() is run before .validate() in .run_validation()
        # it needs to be run again for UniqueTogetherValidator to work with changed attrs
        # TODO: consider overriding .run_validators()
        self.run_validators(attrs)
        return attrs
