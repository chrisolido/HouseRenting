from __future__ import unicode_literals

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpRequest
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet
from rest_framework_mongoengine.viewsets import GenericViewSet as MongoGenericViewSet
from urllib3 import HTTPResponse
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from app.serializers import *
from app.models import Tool, Book, Author, House
from users.models import User
import json
import urllib
import smtplib
from email.mime.text import MIMEText


def index_view(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)


def personal_page_view(request):
    context = {}
    return TemplateResponse(request, 'Personal_Page/personal_information.html', context)


def add_release_view(request):
    context = {}
    return TemplateResponse(request, 'Personal_Page/add_release.html', context)


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


class BadwordView(MongoGenericViewSet):
    @list_route()
    def list(self, request):
        return Response({"HA": "HAA"})

    @detail_route(methods=['post'])
    def bad_worl_filter(self, request):
        if request.method == "POST":
            print(request.POST)
            rent_title = request.POST.get("rent_title", None)
            detail_text = request.POST.get("detail_text", None)

            my_content = str(rent_title) + " " + str(detail_text)

            data = urllib.parse.urlencode(
                {'user-id': 'stucafall', 'api-key': 'pvh6nD5e19etz0TFSE0TSguWanBq7umNUuMtZ6plUtu0gDIH',
                'content': str(my_content)})
            data = data.encode('utf-8')
            request = urllib.request.Request("https://neutrinoapi.com/bad-word-filter")
            request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
            f = urllib.request.urlopen(request, data)
            response = f.read().decode('utf-8')
            print(response)
            result = json.loads(response)

            if result['is-bad']: #have bad words
                to_email_address = "2606449422@qq.com"
                username = "SmallCircle"
                email_topic = "Add House Release Information Fail"
                email_content = ("Dear "+username+", your adding house release information failed"
                            " due to bad words in topic/house_detail, please check on House Renting Website")
                email_inst = Email_Service()
                email_inst.send_email(to_email_address,username,email_topic,email_content)
                return HttpResponse("bad")
                #send an e-mail to user to inform him post failure
            else:
                return HttpResponse("good")
            #Wait for  Manual Check Service

        # print(result['is-bad'])
        # print(result['bad-words-total'])
        # print(result['bad-words-list'])

class Email_Service:
    def send_email(self, to_email_address, username, email_topic, email_content):
        msg_from = '2606449422@qq.com'  #from my email address
        passwd = 'cwnspgrabbfsebjg'  # privilege code
        msg_to = str(to_email_address)  # user's email address

        subject = email_topic  # topic
        content = email_content # content
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465) #qq email server
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
            print ("mail success")
        except s.SMTPException:
            print ("mail failure")
        finally:
            s.quit()

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
        #return Response({"ok": "ok"})


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
