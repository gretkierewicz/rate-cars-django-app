import random
import string

from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from cars.models import Cars


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


def get_post_data_for_car(make, model):
    return {'make': make, 'model_name': model}


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

        cls.urls = {
            'cars-list': "/cars/",
            'cars-popular': f"/cars/popular/",
            **get_urls_for_make(make=cls.instance.make),
            **get_urls_for_model(make=cls.instance.make, model=cls.instance.models.first().name),
        }

        models_list = {
            'HONDA': ['Insight', 'Pilot', 'Ridgeline', ],
            'FORD': ['Thunderbird', 'Edge', 'Turus', ],
        }
        for make, models in models_list.items():
            obj, create = Cars.objects.get_or_create(make=make)
            for model in models:
                obj.models.create(name=model)

    def test_get_endpoints_status_code(self):
        for view, url in self.urls.items():
            with APITestCase.subTest(self, url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_200_OK,
                                 response.get('data') or response.get('errors') or response)

    def test_post_car_model(self):
        APITestCase.skipTest(self, 'time-heavy')
        data = {
            'HONDA': ['Fit', 'CRF250', 'Sportrax'],
            'FORD': ['Escape', 'Focus', 'Fairmont'],
        }
        for make, models in data.items():
            for model in models:
                with APITestCase.subTest(self, f"{make} - {model}"):
                    response = self.client.post(
                        self.urls['cars-list'],
                        data=get_post_data_for_car(make=make, model=model)
                    )
                    self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                                     response.get('data') or response.get('errors') or response)

    def test_post_rate(self):
        for rate in range(1, 5):
            with APITestCase.subTest(self, rate):
                response = self.client.post(self.urls['car-models-rate'], data={'rate': rate})
                self.assertEqual(response.status_code, status.HTTP_200_OK,
                                 response.get('data') or response.get('errors') or response)

    # INVALID section

    def test_get_invalid(self):
        test_urls = {
            'valid make': get_urls_for_make(make=rand_str(k=10)),
            'invalid make & model': get_urls_for_model(make=rand_str(k=10), model=rand_str(k=10)),
            'valid make & invalid model': get_urls_for_model(make=self.instance.make, model=rand_str(k=10)),
        }
        for msg, urls in test_urls.items():
            for view, url in urls.items():
                with APITestCase.subTest(self, f"{msg} - {url}"):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                                     response.get('data') or response.get('errors') or response)

    def test_post_invalid_car(self):
        APITestCase.skipTest(self, 'time-heavy')
        make_data = {
            'empty make': {'make': ''},
            'wrong make': {'make': rand_str()},
            'right make': {'make': 'HONDA'},
        }
        model_data = {
            'empty model': {'model_name': ''},
            'wrong model': {'model_name': rand_str()},
            # right model not matching HONDA car make (FORD's one)
            'right model': {'model_name': 'Tempo'},
        }
        for make_msg, make in make_data.items():
            for model_msg, model in model_data.items():
                with APITestCase.subTest(self, f"{make_msg} - {model_msg}"):
                    response = self.client.post(self.urls['cars-list'], data={**make, **model})
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                                     response.get('data') or response.get('errors') or response)

    def test_post_invalid_rate(self):
        test_data = {
            'less than 1': 0,
            'negative': -2,
            'float': 1.5,
            'more than 5': 6
        }
        for msg, rate in test_data.items():
            with APITestCase.subTest(self, msg):
                response = self.client.post(self.urls['car-models-rate'], data={'rate': rate})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                                 response.get('data') or response.get('errors') or response)
