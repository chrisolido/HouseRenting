from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
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
from rest_framework.reverse import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.models import *
from urllib import parse
from django.core.mail import EmailMessage
import ast
USER = ("user", "{\"user\": \"\", \"auth\": \"\"}")

email = EmailMessage('Subject', 'Body verification code is 423455', to=['kevin.barre@epitech.eu', 'ikelive@hotmail.fr'])


def index_view(request):
    username = json.loads(parse.unquote(request.COOKIES.get(*USER)))
    context = {
        "user": username["user"]
    }
    print(request.COOKIES)
    return TemplateResponse(request, 'index.html', context)


def personal_page_view(request):
    context = {}
    return TemplateResponse(request, 'Personal_Page/personal_information.html', context)


def add_release_view(request):
    context = {}
    return TemplateResponse(request, 'Personal_Page/add_release.html', context)

def personalinfo_view(request):
    context = {}
    return TemplateResponse(request, 'Personal_Page/personal_information.html', context)

def house_detail_view(request):
    context = {}
    return TemplateResponse(request, 'House_detail/HouseDetail.html', context)


# @login_required(redirect_field_name='login')
def manual_check_view(request):
    context = {}
    return TemplateResponse(request, 'Manual_Check/Manual_Check.html', context)


def user_register_view(request):
    context = {}
    if request.method == "POST":
        print(request.POST)
        new_user = User(
            username=request.POST.get("PhoneNumber"),
            email=None,
            name=request.POST.get("username"),
            is_active=True,
            is_staff=False,
            phone=request.POST.get("PhoneNumber")
        )
        new_user.set_password(request.POST.get("setP"))
        new_user.save()
        return HttpResponseRedirect(reverse('index', request=request))
    return TemplateResponse(request, 'House_detail/Register.html', context)


def user_logout_view(request):
    response = HttpResponseRedirect(reverse('index', request=request))
    response.delete_cookie("user")
    return response


def user_login_view(request):
    context = RequestContext(request)
    if request.method == "POST":
        userauth = request.COOKIES.get(*USER)
        userauth = json.loads(parse.unquote(userauth))
        user = authenticate(username=request.POST.get("PhoneNumber"), password=request.POST.get("Password"))
        userauth["user"] = user.name
        userauth["auth"] = str(Token.objects.get_or_create(user=user)[0])
        response = HttpResponseRedirect(reverse('index', request=request))
        response.set_cookie("user", json.dumps(userauth))
        return response
    return TemplateResponse(request, 'House_detail/login.html', context)


class HouseViewSet(MongoModelViewSet):
    lookup_field = 'id'
    serializer_class = HouseSerializer

    def get_queryset(self):
        print(self.request.GET)
        houses = House.objects.all()
        if self.request.GET.get("pricemin"):
            filt = ast.literal_eval(self.request.GET.get("pricemin"))
            print(filt)
            houses = houses.filter(price__gt=filt)
        if self.request.GET.get("pricemax"):
            filt = ast.literal_eval(self.request.GET.get("pricemax"))
            print(filt)
            houses = houses.filter(price__lt=filt)
        if self.request.GET.get("district") and self.request.GET.get("district") != "All":
            filt = self.request.GET.get("district")
            houses = houses.filter(address__district=filt)
        if self.request.GET.get("roomnbr") and self.request.GET.get("roomnbr") != "All":
            filt = ast.literal_eval(self.request.GET.get("roomnbr"))
            print(filt)
            if filt == 99:
                houses = houses.filter(roomnbr__gt=3)
            else:
                houses = houses.filter(roomnbr=filt)
        if self.request.GET.get("renttype") and self.request.GET.get("renttype") != "All":
            filt = self.request.GET.get("renttype")
            print(filt)
            houses = houses.filter(type=filt)
        if self.request.GET.get("search"):
            filt = self.request.GET.get("search")
            houses = houses.filter(information__icontains=filt)
        print(houses)
        return houses


# class HouseViewSet(MongoModelViewSet):
#     """
#     Contains information about inputs/outputs of a single program
#     that may be used in Universe workflows.
#     """
#     lookup_field = 'id'
#     serializer_class = ToolSerializer
#
#     def get_queryset(self):
#         return Tool.objects.all()


class ManualCheckView(viewsets.ViewSet):
    def create(self, request):
        print("ManualCheck")
        if request.method == "POST":
            for house in House.objects.all():
                if not house.check:
                    # return a unchecked house json
                    # from_date_sec = time.mktime(time.strptime(house.from_date, "%Y-%m-%d %H:%M:%S"))
                    # from_date_sec = int(from_date_sec * 1000)
                    # from_date_sec = str(from_date_sec)
                    # print(from_date_sec)
                    # to_date_sec = time.mktime(time.strptime(house.to_date, "%Y-%m-%d %H:%M:%S"))
                    # to_date_sec = int(to_date_sec * 1000)
                    # to_date_sec = str(to_date_sec)

                    print(house.information)
                    rhouse_json = {
                        "title": house.title,
                        "price": house.price,
                        "from_date": str(house.from_date),
                        "to_date": str(house.to_date),
                        "size": house.size,
                        "roomnbr": house.roomnbr,
                        "check": house.check,
                        "information": house.information,
                        "type": house.type,
                        "contact": "5a2e135a59bfed19ea856ff7",
                        "address": {
                            "country": "China",
                            "city": house.address.city,
                            "road": house.address.road,
                            "province": house.address.province,
                            "district": house.address.district,
                            "floor": house.address.floor
                        }
                    }
                    return HttpResponse(json.dumps(rhouse_json), content_type="application/json")
            return HttpResponse("")


class ManualCheckPassView(viewsets.ViewSet):
    def create(self, request):
        print("ManualCheckPass")
        if request.method == "POST":
            title = request.POST.get("title", None)
            for house in House.objects.all():
                if house.title == title:
                    house.check = True
                    house.save()
        return HttpResponse("OK")


class ManualCheckRejectView(viewsets.ViewSet):
    def create(self, request):
        print("ManualCheckReject")
        if request.method == "POST":
            title = request.POST.get("title", None)
            for house in House.objects.all():
                if house.title == title:
                    house.delete()
        return HttpResponse("OK")


class ShowHouseDetailView(viewsets.ViewSet):
    def create(self, request):
        print("ShowHouseDetailView")
        if request.method == "POST":
            title = request.POST.get("title", None)
            for house in House.objects.all():
                if house.title == title:
                    # return this house's detail
                    rhouse_json = {
                        "title": house.title,
                        "price": house.price,
                        "from_date": str(house.from_date),
                        "to_date": str(house.to_date),
                        "size": house.size,
                        "roomnbr": house.roomnbr,
                        "check": house.check,
                        "information": house.information,
                        "type": house.type,
                        "contact": "5a2e135a59bfed19ea856ff7",
                        "address": {
                            "country": "China",
                            "city": house.address.city,
                            "road": house.address.road,
                            "province": house.address.province,
                            "district": house.address.district,
                            "floor": house.address.floor
                        }
                    }
                    return HttpResponse(json.dumps(rhouse_json), content_type="application/json")
        return HttpResponse("OK")


class BadwordView(viewsets.ViewSet):

    def create(self, request):
        print("Bad word")
        if request.method == "POST":
            rent_title = request.POST.get("rent_title", None)
            detail_text = request.POST.get("detail_text", None)
            price = request.POST.get("price", None)
            from_date = time.mktime(time.strptime(request.POST.get("from_date", None), "%Y-%m-%d"))
            from_date = int(from_date * 1000)
            from_date = str(from_date)
            # print(from_date)
            to_date = time.mktime(time.strptime(request.POST.get("to_date", None), "%Y-%m-%d"))
            to_date = int(to_date * 1000)
            to_date = str(to_date)

            size = request.POST.get("size", None)
            roomnbr = request.POST.get("roomnbr", None)
            check = request.POST.get("check", None)
            type = request.POST.get("type", None)
            province = request.POST.get("province", None)
            city = request.POST.get("city", None)
            district = request.POST.get("district", None)
            address = request.POST.get("address", None)
            floor = request.POST.get("floor", None)

            my_content = str(rent_title) + "" + str(detail_text)

            data = urllib.parse.urlencode(
                {'user-id': 'stucafall', 'api-key': 'pvh6nD5e19etz0TFSE0TSguWanBq7umNUuMtZ6plUtu0gDIH',
                 'content': str(my_content)})
            data = data.encode('utf-8')
            request = urllib.request.Request("https://neutrinoapi.com/bad-word-filter")
            request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
            f = urllib.request.urlopen(request, data)
            response = f.read().decode('utf-8')
            # print(response)
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
                # insert house info into DB but check is false
                print("in else")

                house_info = '''
                                [
                                    {
                                    "title":"''' + rent_title + '''",
                                    "price": ''' + price + ''',
                                    "from_date": {"$date": ''' + from_date + '''},
                                    "to_date": {"$date": ''' + to_date + '''},
                                    "size": ''' + size + ''',
                                    "roomnbr": ''' + roomnbr + ''',
                                    "check":''' + check + ''',
                                "information": "''' + detail_text + '''",
                                "type": "''' + type + '''",
                                "contact": "5a2e135a59bfed19ea856ff7",
                                "address": {
                                        "country": "China",
                                        "city": "''' + city + '''",
                                        "road": "''' + address + '''",
                                        "province": "''' + province + '''",
                                        "district": "''' + district + '''",
                                        "floor": ''' + floor + '''
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
    def insert_house_data(self, json_file):
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
