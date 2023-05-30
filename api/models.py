import binascii
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# hook in the New Manager to our Model
class User(AbstractUser):  # from step 2
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = None
    first_name = models.CharField("Անուն", max_length=50)
    last_name = models.CharField("Ազգանուն", max_length=50)
    midle_name = models.CharField("Հայր անուն", max_length=50)
    birth_day = models.DateField(blank=True, null=True)
    phone = models.CharField("Հեռ․ համար", max_length=30)
    address = models.CharField("Հասցե", max_length=100)
    city = models.CharField("Քաղաք", max_length=70)
    email_verified = models.BooleanField("լ․ փոստը հաստատվծ է", default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()
    

    def __str__(self):
        return f"{self.first_name} {self.midle_name} {self.last_name}"

    class Meta:
        verbose_name = "Օկտատեր"
        verbose_name_plural = "Օկտատեր"


class Professions(models.Model):
    """
    This model for doctors shows their working profession.
    """

    title = models.CharField(
        "Ոլորտ",
        max_length=80,
    )
    description = models.TextField(
        "Նկարագրություն",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Ոլորտ"
        verbose_name_plural = "Ոլորտներ"


class Doctor(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doctor",
        verbose_name="Բժիշկ",
    )

    description = models.TextField(
        "Նկարագրություն",
    )
    photo = models.ImageField(
        "Նկար",
        upload_to="imges/doctor_photo/%Y/%m/%d",
    )

    profession = models.ManyToManyField(
        Professions,
        verbose_name="Ոլորտ",
        related_name="doctor",
    )
    top = models.BooleanField("Ցույց տալ գլխավոր էջում", default=False)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Բժիշկ"
        verbose_name_plural = "Բժիշկներ"


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment",
        verbose_name="Օգտատեր",
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="comment",
        verbose_name="Բժիշկ",
    )

    comment = models.TextField(verbose_name="Գրառում")

    date = models.DateTimeField(auto_now_add=True)

    rate = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = "Գրառում"
        verbose_name_plural = "Գրառումներ"


class Licenses(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="licenses"
    )
    image = ResizedImageField(size=[1000, 1000], upload_to="licenses")


class Token(models.Model):
    """
    The default authorization token model.
    """

    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(
        User,
        related_name="token",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    user_ip = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    region = models.CharField(max_length=150, blank=True, null=True)
    timezone = models.CharField(max_length=150, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    device = models.CharField(max_length=100, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    is_email_client = models.BooleanField(default=False)
    is_mobile = models.BooleanField(default=False)
    is_pc = models.BooleanField(default=False)
    is_tablet = models.BooleanField(default=False)
    is_touch_capable = models.BooleanField(default=False)
    os = models.CharField(max_length=100, blank=True, null=True)
    ua_string = models.TextField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    delete_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = "rest_framework.authtoken" not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class Contact(models.Model):
    TYPES_CHOICE = (
        ("1", "Հեռախոսահամար"),
        ("2", "Էլ։ Փոստ"),
        ("3", "LinkedIn"),
        ("4", "Facebook"),
        ("5", "Instagram"),
        ("6", "Telegram"),
        ("7", "YouTube"),
    )
    types = models.CharField("Տիպ", max_length=1, choices=TYPES_CHOICE)
    value = models.TextField("Կոնտակտ")

    @property
    def name(self):
        return self.get_types_display()

    @classmethod
    def get_mobile(cls):
        return cls.objects.filter(types="1")

    @classmethod
    def get_email(cls):
        return cls.objects.filter(types="2")

    @classmethod
    def get_social(cls):
        return cls.objects.all().exclude(types__in=["1", "2"])

    def link(self):
        if self.types == "1":
            return f"tel:{self.value}"
        elif self.types == "2":
            return f"mailto:{self.value}"
        else:
            return self.value

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "կոնտակտ"
        verbose_name_plural = "Կոնտակներ"


class Opinion(models.Model):
    name = models.CharField("Անուն", max_length=50)
    avatar = ResizedImageField(
        "Նկար",
        upload_to="Opinion_avatars",
    )
    status = models.CharField("Ստատուս", max_length=20)
    text = models.TextField("Տեքստ")
    rate = models.IntegerField("Գնահատական", default=5)

    class Meta:
        verbose_name = "կարծիք"
        verbose_name_plural = "Կարծիքներ"

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.TextField(blank=False, null=False)
    answer = models.TextField(blank=False, null=False)
