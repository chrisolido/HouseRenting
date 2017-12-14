from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
import json

from app.models import House

# Create your tests here.


# {
#     "name": "House List",
#     "description": "",
#     "renders": [
#         "application/json",
#         "text/html"
#     ],
#     "parses": [
#         "application/json",
#         "application/x-www-form-urlencoded",
#         "multipart/form-data"
#     ],
#     "actions": {
#         "POST": {
#             "id": {
#                 "type": "field",
#                 "required": false,
#                 "read_only": true,
#                 "label": "Id"
#             },
#             "title": {
#                 "type": "string",
#                 "required": true,
#                 "read_only": false,
#                 "label": "Title"
#             },
#             "price": {
#                 "type": "float",
#                 "required": true,
#                 "read_only": false,
#                 "label": "Price"
#             },
#             "from_date": {
#                 "type": "datetime",
#                 "required": false,
#                 "read_only": false,
#                 "label": "Available  date"
#             },
#             "to_date": {
#                 "type": "datetime",
#                 "required": false,
#                 "read_only": false,
#                 "label": "Available date"
#             },
#             "size": {
#                 "type": "integer",
#                 "required": false,
#                 "read_only": false,
#                 "label": "Room size"
#             },
#             "room": {
#                 "type": "decimal",
#                 "required": false,
#                 "read_only": false,
#                 "label": "Number of room",
#                 "min_value": 0,
#                 "max_value": 10
#             },
#             "information": {
#                 "type": "field",
#                 "required": false,
#                 "read_only": false,
#                 "label": "Description"
#             },
#             "type": {
#                 "type": "choice",
#                 "required": true,
#                 "read_only": false,
#                 "label": "Type",
#                 "choices": [
#                     {
#                         "value": "Group",
#                         "display_name": "Group"
#                     },
#                     {
#                         "value": "Alone",
#                         "display_name": "Alone"
#                     }
#                 ]
#             },
#             "contact": {
#                 "type": "field",
#                 "required": false,
#                 "read_only": false,
#                 "label": "Contact",
#                 "choices": [
#                     {
#                         "value": "1",
#                         "display_name": "kevin"
#                     }
#                 ]
#             },
#             "address": {
#                 "type": "nested object",
#                 "required": false,
#                 "read_only": false,
#                 "label": "Address",
#                 "children": {
#                     "country": {
#                         "type": "string",
#                         "required": true,
#                         "read_only": false,
#                         "label": "Country"
#                     },
#                     "city": {
#                         "type": "string",
#                         "required": true,
#                         "read_only": false,
#                         "label": "City"
#                     },
#                     "road": {
#                         "type": "string",
#                         "required": true,
#                         "read_only": false,
#                         "label": "Road"
#                     },
#                     "province": {
#                         "type": "string",
#                         "required": true,
#                         "read_only": false,
#                         "label": "Province"
#                     },
#                     "district": {
#                         "type": "string",
#                         "required": true,
#                         "read_only": false,
#                         "label": "District"
#                     },
#                     "floor": {
#                         "type": "integer",
#                         "required": true,
#                         "read_only": false,
#                         "label": "Floor"
#                     }
#                 }
#             }
#         }
#     }
# }


# {
#     "title": "",
#     "price": null,
#     "from_date": null,
#     "to_date": null,
#     "size": null,
#     "room": null,
#     "information": null,
#     "type": null,
#     "contact": null,
#     "address": {
#         "country": "",
#         "city": "",
#         "road": "",
#         "province": "",
#         "district": "",
#         "floor": null
#     }
# }

# YYYY,MM,DD,HH,MM,SS,NNNNNN
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

    def setUp(self):
        self.house_list = json.loads(house_info)

    def doCleanups(self):
        for house in House.objects.all():
            print(house.to_json())
        # House.drop_collection()

    def test_add_house(self):
        House.drop_collection()
        for house in self.house_list:
            local_house = House.from_json(json.dumps(house))
            local_house.save()
