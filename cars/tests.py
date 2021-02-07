import json
import random
import string

from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from cars.models import Cars
from cars.serializers import CarsSerializer, CarModelsSerializer


def rand_str(k=10):
    return ''.join(random.choices(string.ascii_letters, k=k))


def get_urls_for_make(make):
    return {
        'cars-detail': f"/cars/{make}/",
        'car-models-list': f"/cars/{make}/models/",
    }


def get_urls_for_model(make, model):
    return {
        'car-models-detail': f"/cars/{make}/models/{model}/",
        'car-models-rate': f"/cars/{make}/models/{model}/rate/",
    }


class CarsTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Fill all this data for tests to work properly
        """
        cls.client = APIClient()
        cls.factory = APIRequestFactory()

        cls.instance = Cars.objects.create(make='HONDA')
        cls.instance.models.create(name='Civic')

        models_list = {
            'HONDA': ['Insight', 'Pilot', 'Ridgeline', ],
            'FORD': ['Thunderbird', 'Edge', 'Turus', ],
        }
        for make, models in models_list.items():
            obj, create = Cars.objects.get_or_create(make=make)
            for model in models:
                obj.models.create(name=model)

        cls.valid_urls = {
            'cars-list': "/cars/",
            'cars-popular': f"/cars/popular/",
            **get_urls_for_make(make=cls.instance.make),
            **get_urls_for_model(make=cls.instance.make, model=cls.instance.models.first().name),
        }

        cls.valid_car_data = {
            'make': 'HONDA',
            'models': [
                {'name': 'Passport'},
                {'name': 'Shadow'},
                {'name': 'Odyssey'},
            ]
        }

        cls.valid_rates = range(1, 5)

        cls.invalid_urls = {
            'invalid make': get_urls_for_make(make=rand_str(k=10)),
            'invalid make & model': get_urls_for_model(make=rand_str(k=10), model=rand_str(k=10)),
            'valid make & invalid model': get_urls_for_model(make=cls.instance.make, model=rand_str(k=10)),
        }

        cls.invalid_car_data = {
            'make_data': {
                'empty': {'make': ''},
                'wrong': {'make': rand_str()},
                'right': {'make': 'HONDA'},
            },
            'model_data': {
                'empty': {'model_name': ''},
                'wrong': {'model_name': rand_str()},
                # right model not matching HONDA car make (FORD's one)
                'for different make': {'model_name': 'Tempo'},
            }
        }

        cls.invalid_rates = {
            'less than 1': 0,
            'negative': -2,
            'float type': 1.5,
            'more than 5': 6
        }

    # VALID section

    def test_status_code_get_valid(self):
        for view, url in self.valid_urls.items():
            with APITestCase.subTest(self, f"url: {url}"):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_200_OK, response.data or response)

    def test_data_get_list(self):
        response = self.client.get(self.valid_urls['cars-list'])
        self.assertJSONEqual(
            json.dumps(response.data),
            CarsSerializer(instance=Cars.objects.all(), many=True, context={'request': self.factory.get('')}).data,
            response.data or response
        )

    def test_data_get_car_make(self):
        response = self.client.get(self.valid_urls['cars-detail'])
        self.assertJSONEqual(
            json.dumps(response.data),
            CarsSerializer(instance=self.instance, context={'request': self.factory.get('')}).data,
            response.data or response
        )

    def test_data_get_car_model(self):
        response = self.client.get(self.valid_urls['car-models-detail'])
        self.assertJSONEqual(
            json.dumps(response.data),
            CarModelsSerializer(instance=self.instance.models.first(), context={'request': self.factory.get('')}).data,
            response.data or response
        )

    def test_status_code_post_valid_car(self):
        response = self.client.post(
            self.valid_urls['cars-list'],
            data=json.dumps(self.valid_car_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data or response)

    def test_status_code_post_valid_rate(self):
        for rate in self.valid_rates:
            with APITestCase.subTest(self, f"rate: {rate}"):
                response = self.client.post(self.valid_urls['car-models-rate'], data={'rate': rate})
                self.assertEqual(response.status_code, status.HTTP_200_OK, response.data or response)

    def test_status_code_delete_valid_car_make(self):
        response = self.client.delete(self.valid_urls['cars-detail'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data or response)

    def test_status_code_delete_valid_car_model(self):
        response = self.client.delete(self.valid_urls['car-models-detail'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data or response)

    # INVALID section

    def test_status_code_get_invalid_car(self):
        for msg, urls in self.invalid_urls.items():
            for view, url in urls.items():
                with APITestCase.subTest(self, f"{msg} url: {url}"):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.data or response)

    def test_status_code_post_invalid_car(self):
        for make_msg, make in self.invalid_car_data['make_data'].items():
            for model_msg, model in self.invalid_car_data['model_data'].items():
                with APITestCase.subTest(self, f"make: {make_msg}; model: {model_msg}"):
                    response = self.client.post(self.valid_urls['cars-list'], data={**make, **model})
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data or response)

    def test_status_code_post_invalid_rate(self):
        for msg, rate in self.invalid_rates.items():
            with APITestCase.subTest(self, f"rate: {msg}"):
                response = self.client.post(self.valid_urls['car-models-rate'], data={'rate': rate})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data or response)

    def test_status_code_delete_invalid_car(self):
        for msg, urls in self.invalid_urls.items():
            for view, url in urls.items():
                with APITestCase.subTest(self, f"{msg} url: {url}"):
                    response = self.client.delete(self.valid_urls['cars-detail'])
                    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, response.data or response)
