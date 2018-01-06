from rest_framework import views, mixins, permissions, exceptions
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from rest_framework import parsers, renderers
from django.middleware.csrf import get_token
from users.serializers import *
from users.models import *
from users.authentication import TokenAuthentication


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    Read-only User endpoint
    """
    permission_classes = (permissions.IsAuthenticated,)  # IsAdminUser?
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class ObtainAuthToken(views.APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (TokenAuthentication,)
    # parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    # renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    def get(self, request, *arg, **kwargs):
        return Response({"csrfmiddlewaretoken": get_token(request)})


obtain_auth_token = ObtainAuthToken.as_view()
