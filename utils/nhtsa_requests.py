import requests


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
