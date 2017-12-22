from __future__ import unicode_literals

from django.template.response import TemplateResponse

from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet

from app.serializers import *
from app.models import Tool, Book, Author, House
from users.models import User


def index_view(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)

def personal_page_view(request):
    context = {}
    return TemplateResponse(request, 'Personal_Page/personal_information.html', context)


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
