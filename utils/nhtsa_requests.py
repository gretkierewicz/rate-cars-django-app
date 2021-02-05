import requests


def get_make_name_max_len():
    """
    Function to check max len of car's make name
    result = 72 (05 FEB 2021)
    """
    response = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json')
    return max([len(_.get('Make_Name')) for _ in response.json().get('Results')])


def get_model_name_max_len():
    """
    HEAVY! Function to check max len of car's model name
    result = 136 (05 FEB 2021)
    """
    max_len = 0
    list_response = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json')
    for make in [_.get('Make_Name') for _ in list_response.json().get('Results')]:
        response = requests.get(f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make}?format=json')
        try:
            _ = max([len(_.get('Model_Name')) for _ in response.json().get('Results')])
            max_len = _ if _ > max_len else max_len
        except:
            continue
    return max_len


class CarsModelsForMake:
    """
    Simple class pulling data from https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make} endpoint
    nhtsa endpoint description:
    This returns the Models in the vPIC dataset for a specified Make whose name is LIKE the Make in vPIC Dataset.
    Make can be a partial, or a full for more specificity (e.g., "Harley", "Harley Davidson", etc.)
    """
    def __init__(self, make_name):
        response = requests.get(f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make_name}?format=json')
        results = response.json().get('Results')

        self.make_name = results[0].get('Make_Name') if results else None
        self.models = [_.get('Model_Name') for _ in results]
