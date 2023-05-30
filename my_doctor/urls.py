from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from api.views import (
    ChangePasswordView,
    DoctorViewSet,
    FAQListViewSdet,
    GlobalApiVewSet,
    IndexApiViewSet,
    LoginViewSet,
    LogoutViewSet,
    ProfessionsViewSet,
    RegisterViewSet,
    email_verification,
)
from chat.views import ChatViewSet
from evants.views import EvantsViewSet
from blog.views import ArticleViewSet

router = routers.DefaultRouter()
router.register("professions", ProfessionsViewSet, basename="professions")
router.register("doctors", DoctorViewSet)
router.register("auth/register", RegisterViewSet, basename="register")
router.register("auth/logout", LogoutViewSet, basename="logout")
router.register("auth/evants", EvantsViewSet, basename="evants")
router.register("auth/login", LoginViewSet, basename="login")
router.register(
    "auth/changepassword", ChangePasswordView, basename="passwordChange"
)
router.register("global", GlobalApiVewSet, basename="Global")
router.register("auth/chat", ChatViewSet, basename="chat")
router.register("index", IndexApiViewSet, basename="index")
router.register("blog", ArticleViewSet)
router.register("FAQ", FAQListViewSdet, basename="FAQ")

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = (
    [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
        path("", include(router.urls)),
        path(
            "activate/<code>/",
            email_verification,
            name="active",
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
