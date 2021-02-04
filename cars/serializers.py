from rest_framework.serializers import HyperlinkedModelSerializer

from cars.models import Cars


class CarsSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Cars
        fields = '__all__'
