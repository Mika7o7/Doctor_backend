from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from evants.serializers import EvantsSerializer

from .models import (
    FAQ,
    Comment,
    Contact,
    Doctor,
    Opinion,
    Professions,
    Token,
    User,
)


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * email
      * password.
    It will try to authenticate the user with when validated.
    """

    email = serializers.EmailField(label="Email", write_only=True)
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        # Take email and password from request
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = "Access denied: wrong username or password."
                raise serializers.ValidationError(msg, code="authorization")
            if not getattr(user, "email_verified", False):  # type: ignore
                msg = "Please check your email for confirmation"
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code="authorization")
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs["user"] = user
        attrs["token"] = Token.objects.create(user=user)
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    password2 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "midle_name",
            "address",
            "city",
            "phone",
            "email",
            "password",
            "password2",
        )

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            midle_name=validated_data["midle_name"],
            city=validated_data["city"],
            address=validated_data["address"],
            phone=validated_data["phone"],
        )
        if validated_data["password2"] == validated_data["password"]:
            user.set_password(validated_data["password"])
            user.save()

        return user


class ProfessionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Professions
        fields = [
            "title_hy",
            "title_ru",
            "title_en",
            "description_hy",
            "description_ru",
            "description_en",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "midle_name",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "comment",
            "rate",
            "date",
        ]


class DoctorSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profession = ProfessionsSerializers(read_only=True, many=True)
    comment = CommentSerializer(read_only=True, many=True)
    evants = EvantsSerializer(read_only=True, many=True)

    class Meta:
        model = Doctor
        comments = Comment
        fields = [
            "url",
            "user",
            "description_hy",
            "description_ru",
            "description_en",
            "photo",
            "profession",
            "comment",
            "evants",
        ]


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        if attrs["old_password"] == attrs["password"]:
            raise serializers.ValidationError(
                {"password": "Old and new passwors are matching."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("id", "name", "link")


class DoctorMinInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    profession = ProfessionsSerializers(read_only=True, many=True)

    class Meta:
        model = Doctor
        fields = ("id", "user", "photo", "profession")


class OpinionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = (
            "id",
            "name_hy",
            "name_ru",
            "name_en",
            "status",
            "avatar",
            "rate",
            "text_hy",
            "text_ru",
            "text_en",
        )


class FAQSerialazer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            "id",
            "question_hy",
            "question_ru",
            "question_en",
            "answer_hy",
            "answer_ru",
            "answer_en",
        ]
