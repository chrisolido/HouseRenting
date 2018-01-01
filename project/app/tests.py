from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
import json

from app.models import House

# Create your tests here.

house_info = '''
[
    {
        "title":"Big House",
        "price": 56.0,
        "from_date": {"$date": 1512980682785},
        "to_date": {"$date": 1512980682785},
        "size": 3,
        "information": null,
        "type": "Group",
        "contact": "5a2e135a59bfed19ea856ff7",
        "check": false,
        "address": {
            "country": "China",
            "city": "Shanghai",
            "road": "879",
            "province": "Shanghai",
            "district": "Luwan",
            "floor": 4
        }
    },
    {
        "title":"Funy house",
        "price": 546.0,
        "from_date": {"$date": 1512980682785},
        "to_date": {"$date": 1512980682785},
        "size": 5,
        "check": true,
        "information": "Information of house",
        "type": "Group",
        "contact": "5a2e135a59bfed19ea856ff7",
        "address": {
            "country": "China",
            "city": "Shanghai",
            "road": "88",
            "province": "Shanghai",
            "district": "Xuhui",
            "floor": 1
        }
    }
]
'''


class HouseViewSetTestCase(APITestCase):

    house_list = None

    def setUp(self): #first
        self.house_list = json.loads(house_info)

    def doCleanups(self): #last
        for house in House.objects.all():
            print(house.to_json())
        # House.drop_collection()

    def test_add_house(self):
        House.drop_collection()
        for house in self.house_list:
            local_house = House.from_json(json.dumps(house))
            local_house.save()

    def test_is_check(self):
        for house in House.objects.all():
            if house.check:
                print("House has been checked")
            else:
                print("Tou need check")
