from .settings_base import *  # noqa

ADMIN_URL = env("ADMIN_URL")  # noqa

INSTALLED_APPS = [
    "django_cleanup",
    "modeltranslation",
    "baton",
    "rest_framework.authtoken",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ckeditor",
    "api",
    "chat",
    "evants",
    "blog",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "my_doctor.urls_admin"


CKEDITOR_JQUERY_URL = (
    "https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"
)

CKEDITOR_CONFIGS = {
    "default": {
        "width": "100%",
        "height": 600,
        "toolbar_YourCustomToolbarConfig": [
            {
                "name": "document",
                "items": [
                    "Source",
                    "-",
                    "Save",
                    "NewPage",
                    "Preview",
                    "Print",
                    "-",
                    "Templates",
                ],
            },
            {
                "name": "clipboard",
                "items": [
                    "Cut",
                    "Copy",
                    "Paste",
                    "PasteText",
                    "PasteFromWord",
                    "-",
                    "Undo",
                    "Redo",
                ],
            },
            {
                "name": "editing",
                "items": ["Find", "Replace", "-", "SelectAll"],
            },
            {
                "name": "forms",
                "items": [
                    "Form",
                    "Checkbox",
                    "Radio",
                    "TextField",
                    "Textarea",
                    "Select",
                    "Button",
                    "ImageButton",
                    "HiddenField",
                ],
            },
            "/",
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "RemoveFormat",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "CreateDiv",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                    "-",
                    "BidiLtr",
                    "BidiRtl",
                    "Language",
                ],
            },
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
            {
                "name": "insert",
                "items": [
                    "Image",
                    "Flash",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "SpecialChar",
                    "PageBreak",
                    "Iframe",
                ],
            },
            "/",
            {
                "name": "styles",
                "items": ["Styles", "Format", "Font", "FontSize"],
            },
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "tools", "items": ["Maximize", "ShowBlocks"]},
        ],
        "toolbar": "YourCustomToolbarConfig",
    },
}

# BATON = {
#     "SITE_HEADER": "Baton",
#     "SITE_TITLE": "Baton",
#     "INDEX_TITLE": "Site administration",
#     "SUPPORT_HREF": "https://github.com/otto-torino/django-baton/issues",
#     "COPYRIGHT": 'copyright © 2020 <a href="https://www.otto.to.it">Otto srl</a>',  # noqa
#     "POWERED_BY": '<a href="https://www.otto.to.it">Otto srl</a>',
#     "CONFIRM_UNSAVED_CHANGES": True,
#     "SHOW_MULTIPART_UPLOADING": True,
#     "ENABLE_IMAGES_PREVIEW": True,
#     "CHANGELIST_FILTERS_IN_MODAL": True,
#     "CHANGELIST_FILTERS_ALWAYS_OPEN": False,
#     "CHANGELIST_FILTERS_FORM": True,
#     "MENU_ALWAYS_COLLAPSED": False,
#     "MENU_TITLE": "Menu",
#     "MESSAGES_TOASTS": False,
#     "GRAVATAR_DEFAULT_IMG": "retro",
#     "LOGIN_SPLASH": "/static/core/img/login-splash.png",
#     "SEARCH_FIELD": {
#         "label": "Search contents...",
#         "url": "/search/",
#     },
#     "MENU": (
#         {"type": "title", "label": "main", "apps": ("auth",)},
#         {
#             "type": "app",
#             "name": "auth",
#             "label": "Authentication",
#             "icon": "fa fa-lock",
#             "models": (
#                 {"name": "user", "label": "Users"},
#                 {"name": "group", "label": "Groups"},
#             ),
#         },
#         {"type": "title", "label": "Contents", "apps": ("flatpages",)},
#         {
#             "type": "model",
#             "label": "Pages",
#             "name": "flatpage",
#             "app": "flatpages",
#         },
#         {
#             "type": "free",
#             "label": "Custom Link",
#             "url": "http://www.google.it",
#             "perms": ("flatpages.add_flatpage", "auth.change_user"),
#         },
#         {
#             "type": "free",
#             "label": "My parent voice",
#             "default_open": True,
#             "children": [
#                 {
#                     "type": "model",
#                     "label": "A Model",
#                     "name": "mymodelname",
#                     "app": "myapp",
#                 },
#                 {
#                     "type": "free",
#                     "label": "Another custom link",
#                     "url": "http://www.google.it",
#                 },
#             ],
#         },
#     ),
# }
