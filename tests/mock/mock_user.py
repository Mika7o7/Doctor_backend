from api.models import City


def create_user_data(**kwargs):
    return {
        "email": kwargs.get("email", "test2@test.test"),
        "password": kwargs.get("password", "123aaa123"),
        "first_name": kwargs.get("first_name", "a"),
        "last_name": kwargs.get("last_name", "a"),
        "midle_name": kwargs.get("midle_name", "a"),
        "city": kwargs.get("city", City.objects.create().id),
        "address": kwargs.get("address", "a"),
        "phone": kwargs.get("phone", "2345678"),
    }
