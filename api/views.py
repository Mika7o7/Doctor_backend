from datetime import datetime
from typing import Any, Dict

from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponseRedirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from blog.models import Article
from blog.serializers import ArticleSerializer
from my_doctor.utils import (
    decode_from_base64,
    encode_to_md5,
    get_client_ip,
    get_user_agent,
)

from .models import FAQ, Contact, Doctor, Opinion, Professions, Token, User
from .serializers import (
    ChangePasswordSerializer,
    ContactSerializer,
    DoctorMinInfoSerializer,
    DoctorSerializers,
    FAQSerialazer,
    LoginSerializer,
    OpinionInfoSerializer,
    ProfessionsSerializers,
    RegisterSerializer,
)
from .tasks import send_email_funq


def email_verification(request, code: str) -> HttpResponseRedirect:
    try:
        id, md5_data = decode_from_base64(code)
        user = User.objects.get(pk=int(id))
        if md5_data == encode_to_md5(user.email, str(user.date_joined)):
            user.email_verified = True
            user.save()
            return HttpResponseRedirect(settings.FRONTEND_URL)
        # TODO: add invalid data page url
        return HttpResponseRedirect("invalid data page")
    except User.DoesNotExist:
        # TODO: add user not exist page url
        return HttpResponseRedirect("user not exist page")
    except Exception:
        # TODO: add error page url
        return HttpResponseRedirect("Error Page")


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializers


class ProfessionsViewSet(viewsets.ModelViewSet):
    queryset = Professions.objects.all()
    serializer_class = ProfessionsSerializers


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    http_method_names = ["post", "options"]

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        print(user)
        send_email_funq.delay(
            user.id,
            user.email,
            str(user.date_joined),
        )  # type: ignore
        return Response(
            {"token": token.key, "email": user.email},
            status=status.HTTP_201_CREATED,
        )


class LoginViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "options"]
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def create(self, request) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]  # type: ignore
        if not user.is_active:
            return Response(
                {
                    "User is not active:": "Pleas check your email \
                    and activate your account."
                },
                status=status.HTTP_202_ACCEPTED,
            )
        login(request, user)
        token_object = serializer.validated_data["token"]  # type: ignore
        ip_data = get_client_ip(request)
        ua_data = get_user_agent(request)
        token_object.user_ip = ip_data.get("ip", None)
        token_object.country = ip_data.get("country", None)
        token_object.region = ip_data.get("region", None)
        token_object.timezone = ip_data.get("timezone", None)
        if ua_data:
            token_object.browser = ua_data.get_browser()
            token_object.device = ua_data.get_device()
            token_object.is_bot = ua_data.is_bot
            token_object.is_email_client = ua_data.is_email_client
            token_object.is_mobile = ua_data.is_mobile
            token_object.is_pc = ua_data.is_pc
            token_object.is_tablet = ua_data.is_tablet
            token_object.is_touch_capable = ua_data.is_touch_capable
            token_object.os = ua_data.get_os()
            token_object.ua_string = ua_data.ua_string
        token_object.save()

        user_data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "sure_name": user.midle_name,
        }
        return Response(
            {
                "token": token_object.key,
                "user_ info": user_data,
            },
            status=status.HTTP_202_ACCEPTED,
        )


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def create(self, request) -> Response:
        request.auth.deleted = True
        request.auth.delete_date = datetime.now()
        request.auth.save()

        return Response({"code": status.HTTP_200_OK})


class ChangePasswordView(viewsets.ViewSet):
    http_method_names = ["post", "options"]

    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["password"])
        request.user.save()
        return Response({"code": status.HTTP_200_OK})


class GlobalApiVewSet(viewsets.ViewSet):
    def list(self, request):
        data = dict()
        data["contacts"] = {
            "mobile": ContactSerializer(
                Contact.get_mobile(),
                many=True,
                read_only=True,
                context={"request": request},
            ).data,
            "email": ContactSerializer(
                Contact.get_email(),
                many=True,
                read_only=True,
                context={"request": request},
            ).data,
            "social": ContactSerializer(
                Contact.get_social(),
                many=True,
                read_only=True,
                context={"request": request},
            ).data,
        }
        return Response(data, status=status.HTTP_200_OK)


class IndexApiViewSet(viewsets.ViewSet):
    def list(self, request: HttpRequest) -> Response:
        data: Dict[str, Any] = dict()
        data["best_doctors"] = DoctorMinInfoSerializer(
            Doctor.objects.filter(top=True),
            read_only=True,
            many=True,
            context={"request": request},
        ).data
        data["opinions"] = OpinionInfoSerializer(
            Opinion.objects.all(),
            read_only=True,
            many=True,
            context={"request": request},
        ).data
        data["last_news"] = ArticleSerializer(
            Article.objects.all()[:10],
            read_only=True,
            many=True,
            context={"request": request},
        ).data
        return Response(data, status=status.HTTP_200_OK)


class FAQListViewSdet(viewsets.ViewSet):
    def list(self, request):
        queryset = FAQ.objects.all()
        serializer = FAQSerialazer(queryset, many=True)
        return Response(serializer.data)
