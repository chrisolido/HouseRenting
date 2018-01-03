from __future__ import unicode_literals

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpRequest
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet
from rest_framework_mongoengine.viewsets import GenericViewSet as MongoGenericViewSet
from urllib3 import HTTPResponse
from rest_framework.response import Response
from app.serializers import *
from app.models import Tool, Book, Author, House
from users.models import User
import json
import urllib
import smtplib
import time
from email.mime.text import MIMEText
from rest_framework import viewsets


def index_view(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)


def personal_page_view(request):
    context = {}
    return TemplateResponse(request, 'Personal_Page/personal_information.html', context)


def add_release_view(request):
    context = {}
    return TemplateResponse(request, 'Personal_Page/add_release.html', context)

def house_detail_view(request):
    context = {}
    return TemplateResponse(request, 'House_detail/HouseDetail.html', context)

def manual_check_view(request):
    context = {}
    return TemplateResponse(request, 'Manual_Check/Manual_Check.html', context)

def user_register_view(request):
    context = {}
    if request.method == "POST":
        print(request.POST)
    return TemplateResponse(request, 'House_detail/Register.html', context)


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


class BadwordView(viewsets.ViewSet):

    def create(self, request):
        print("Bad word")
        if request.method == "POST":
            print(request.POST)
            rent_title = request.POST.get("rent_title", None)
            detail_text = request.POST.get("detail_text", None)
            price = request.POST.get("price", None)
            from_date = time.mktime(time.strptime(request.POST.get("from_date", None), "%Y-%m-%d"))
            from_date = int(from_date*1000)
            from_date = str(from_date)
            #print(from_date)
            to_date = time.mktime(time.strptime(request.POST.get("to_date", None), "%Y-%m-%d"))
            to_date = int(to_date * 1000)
            to_date = str(to_date)

            size = request.POST.get("size", None)
            check = request.POST.get("check", None)
            type = request.POST.get("type", None)
            province = request.POST.get("province", None)
            city = request.POST.get("city", None)
            district = request.POST.get("district", None)
            address = request.POST.get("address", None)
            floor = request.POST.get("floor", None)

            my_content = str(rent_title) + " " + str(detail_text)

            data = urllib.parse.urlencode(
                {'user-id': 'stucafall', 'api-key': 'pvh6nD5e19etz0TFSE0TSguWanBq7umNUuMtZ6plUtu0gDIH',
                 'content': str(my_content)})
            data = data.encode('utf-8')
            request = urllib.request.Request("https://neutrinoapi.com/bad-word-filter")
            request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
            f = urllib.request.urlopen(request, data)
            response = f.read().decode('utf-8')
            #print(response)
            result = json.loads(response)

            if result['is-bad']:  # have bad words
                to_email_address = "2606449422@qq.com"
                username = "SmallCircle"
                email_topic = "Add House Release Information Fail"
                email_content = ("Dear " + username + ", your adding house release information failed"
                                                      " due to bad words in topic/house_detail, please check on House Renting Website")
                email_inst = Email_Service()
                email_inst.send_email(to_email_address, username, email_topic, email_content)
                return HttpResponse("bad")
                # send an e-mail to user to inform him post failure
            else:
                #insert house info into DB but check is false
                print("in else")

                house_info = '''
                                [
                                    {
                                    "title":"'''+rent_title+'''",
                                    "price": '''+price+''',
                                    "from_date": {"$date": '''+from_date+'''},
                                    "to_date": {"$date": '''+to_date+'''},
                                    "size": '''+size+''',
                                    "check":'''+check+''',
                                "information": "'''+detail_text+'''",
                                "type": "'''+type+'''",
                                "contact": "5a2e135a59bfed19ea856ff7",
                                "address": {
                                        "country": "China",
                                        "city": "'''+city+'''",
                                        "road": "'''+address+'''",
                                        "province": "'''+province+'''",
                                        "district": "'''+district+'''",
                                        "floor": '''+floor+'''
                                        }
                                    }
                                ]
                                '''
                print(house_info)
                house_list = json.loads(house_info)
                insert_inst = Insert_Service()
                insert_inst.insert_house_data(house_list)

                return HttpResponse("good")
            # Wait for  Manual Check Service

class Insert_Service:
    def insert_house_data(self,json_file):
        for house in json_file:
            local_house = House.from_json(json.dumps(house))
            local_house.save()
        for house in House.objects.all():
            print(house.title)

class Email_Service:
    def send_email(self, to_email_address, username, email_topic, email_content):
        msg_from = '2606449422@qq.com'  # from my email address
        passwd = 'cwnspgrabbfsebjg'  # privilege code
        msg_to = str(to_email_address)  # user's email address

        subject = email_topic  # topic
        content = email_content  # content
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # qq email server
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to, msg.as_string())
            print("mail success")
        except s.SMTPException:
            print("mail failure")
        finally:
            s.quit()

# class ToolViewSet(MongoModelViewSet):
#     """
#     Contains information about inputs/outputs of a single program
#     that may be used in Universe workflows.
#     """
#     lookup_field = 'id'
#     serializer_class = ToolSerializer
#
#     def get_queryset(self):
#         return Tool.objects.all()
#
#
# class BookViewSet(MongoModelViewSet):
#     lookup_field = 'id'
#     serializer_class = BookSerializer
#
#     def get_queryset(self):
#         return Book.objects.all()
#
#
# class AuthorViewSet(MongoModelViewSet):
#     lookup_field = 'id'
#     serializer_class = AuthorSerializer
#
#     def get_queryset(self):
#         return Author.objects.all()
