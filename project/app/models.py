from mongoengine import Document, EmbeddedDocument, fields
from users.models import User


class Author(Document):
    name = fields.StringField()


class Book(Document):
    name = fields.StringField()
    author = fields.ReferenceField(Author, dbref=True)


class ToolInput(EmbeddedDocument):
    id = fields.StringField(required=True)
    type = fields.ListField(fields.DynamicField(null=True))
    label = fields.StringField(required=True, null=True)
    description = fields.StringField(required=False, null=True)
    default = fields.DynamicField(required=False)
    inputBinding = fields.DynamicField(required=True)
    required = fields.BooleanField(required=False, default=True)


class ToolOutput(EmbeddedDocument):
    id = fields.StringField(required=True)
    type = fields.ListField(fields.DynamicField(null=True))
    label = fields.StringField(required=False)
    default = fields.DynamicField(required=False, null=True)
    description = fields.StringField(required=False)
    outputBinding = fields.DynamicField(required=False)
    required = fields.BooleanField(required=False, default=True)


class Tool(Document):
    id = fields.StringField(required=True, primary_key=True)
    # 'class' is a reserved word in python, so to get a field called "class", we use the following trick with vars():
    vars()['class'] = fields.StringField(verbose_name="class", required=True)
    label = fields.StringField(required=True)
    description = fields.StringField(required=True, null=True)
    owner = fields.ListField(fields.StringField())
    contributor = fields.ListField(fields.StringField())
    inputs = fields.EmbeddedDocumentListField(ToolInput)
    outputs = fields.EmbeddedDocumentListField(ToolOutput)
    baseCommand = fields.DynamicField(required=True)
    arguments = fields.DynamicField(required=True)
    requirements = fields.DynamicField(required=True, null=True)
    hints = fields.DynamicField(required=False, null=True)
    cwlVersion = fields.StringField(required=False, null=True, choices=['cwl:draft-2'])
    stdin = fields.StringField(required=False, null=True)
    stdout = fields.StringField(required=False, null=True)
    successCodes = fields.ListField(fields.IntField(), required=False)
    temporaryFailCodes = fields.ListField(fields.IntField(), required=False)
    permanentFailCodes = fields.ListField(fields.IntField(), required=False)


class Address(EmbeddedDocument):
    country = fields.StringField(required=True)
    city = fields.StringField(required=True)
    road = fields.StringField(required=True)
    province = fields.StringField(required=True)
    district = fields.StringField(required=True)
    floor = fields.IntField(required=True)


class House(Document):
    contact = fields.ReferenceField(User, dbref=True)
    title = fields.StringField(required=True, verbose_name="Title")
    price = fields.FloatField(required=True, verbose_name="Price")
    address = fields.EmbeddedDocumentField(Address)
    from_date = fields.DateTimeField(verbose_name="Available  date")
    to_date = fields.DateTimeField(verbose_name="Available date")
    size = fields.IntField(verbose_name="room size")
    room = fields.DecimalField(min_value=0, max_value=10, default=0, precision=0, verbose_name="Number of room")
    information = fields.DynamicField(verbose_name="Description")
    vars()['type'] = fields.StringField(required=True, choices=['Group', 'Alone'])
    # pictures = fields.ListField(fields.ImageField(), required=False)