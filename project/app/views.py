from __future__ import unicode_literals

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpRequest
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet
from urllib3 import HTTPResponse

from app.serializers import *
from app.models import Tool, Book, Author, House
from users.models import User
import json
import urllib


def index_view(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)


def personal_page_view(request):
    context = {}
    return TemplateResponse(request, 'Personal_Page/personal_information.html', context)


def add_release_view(request):
    context = {}
    return TemplateResponse(request, 'Personal_Page/add_release.html', context)


def auto_badword_filter(request):
    print("value")

    if request.method == "GET":
        return HttpResponse("Ok")

    if request.method == "POST":
        print ('blabla')
        print(request.POST)
        rent_title = request.POST.get("rent_title", None)
        detail_text = request.POST.get("detail_text", None)
        #
        my_content = str(rent_title)+ " " +str(detail_text)
        url = 'https://neutrinoapi.com/bad-word-filter'
        params = {
            'user-id': 'stucafall',
            'api-key': 'pvh6nD5e19etz0TFSE0TSguWanBq7umNUuMtZ6plUtu0gDIH',
            'content': str(my_content)
        }

        # param = urllib.parse.urlencode(params)
        # params = params.encode('utf-8')
        # response = urllib.request.urlopen(url % param)
        # print(response.read().decode('utf-8'))
        # result = json.loads(response.read())
        data = urllib.parse.urlencode({'user-id': 'stucafall', 'api-key': 'pvh6nD5e19etz0TFSE0TSguWanBq7umNUuMtZ6plUtu0gDIH', 'content': str(my_content)})
        data = data.encode('utf-8')
        request = urllib.request.Request("https://neutrinoapi.com/bad-word-filter")
        request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
        f = urllib.request.urlopen(request, data)
        print(f.read().decode('utf-8'))

        # print(result['is-bad'])
        # print(result['bad-words-total'])
        # print(result['bad-words-list'])
        #
        return HttpResponse("ok")

    return HttpResponse("Get request")


class HouseViewSet(MongoModelViewSet):
    lookup_field = 'id'
    serializer_class = HouseSerializer

    def get_queryset(self):
        print(self.request.GET)
        print(House.objects.filter(address__country="China"))
        houses = House.objects.filter(address__country="China")
        userid = None
        for user in User.objects.all():
            # userid = user.id
            print(user.id)
        for house in houses:
            # house.update(contact=userid)
            house.save()
            print(User.objects.filter(id=house.contact.id))
        return House.objects.all()


class ToolViewSet(MongoModelViewSet):
    """
    Contains information about inputs/outputs of a single program
    that may be used in Universe workflows.
    """
    lookup_field = 'id'
    serializer_class = ToolSerializer

    def get_queryset(self):
        return Tool.objects.all()


class BookViewSet(MongoModelViewSet):
    lookup_field = 'id'
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.all()


class AuthorViewSet(MongoModelViewSet):
    lookup_field = 'id'
    serializer_class = AuthorSerializer

    def get_queryset(self):
        return Author.objects.all()
