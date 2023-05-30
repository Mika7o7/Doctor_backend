from collections import namedtuple

from . import ua_parser as user_agent_parser
from ._info import (
    EMAIL_PROGRAM_FAMILIES,
    MOBILE_BROWSER_FAMILIES,
    MOBILE_DEVICE_FAMILIES,
    MOBILE_OS_FAMILIES,
    PC_OS_FAMILIES,
    TABLET_DEVICE_BRANDS,
    TABLET_DEVICE_FAMILIES,
    TOUCH_CAPABLE_DEVICE_FAMILIES,
    TOUCH_CAPABLE_OS_FAMILIES,
)


def parse_version(major=None, minor=None, patch=None, patch_minor=None):
    major = major
    minor = minor
    patch = patch
    patch_minor = patch_minor

    return tuple(
        filter(lambda x: x is not None, (major, minor, patch, patch_minor))
    )


OperatingSystem = namedtuple(
    "OperatingSystem", ["family", "version", "version_string"]
)


def parse_operating_system(
    family, major=None, minor=None, patch=None, patch_minor=None
):
    version = parse_version(major, minor, patch)
    version_string = ".".join([str(v) for v in version])
    return OperatingSystem(family, version, version_string)


Browser = namedtuple("Browser", ["family", "version", "version_string"])


def parse_browser(family, major=None, minor=None, patch=None, patch_minor=None):
    # Returns a browser object
    version = parse_version(major, minor, patch)
    version_string = ".".join([str(v) for v in version])
    return Browser(family, version, version_string)


Device = namedtuple("Device", ["family", "brand", "model"])


def parse_device(family, brand, model):
    return Device(family, brand, model)


class UserAgent(object):
    def __init__(self, user_agent_string):
        ua_dict = user_agent_parser.Parse(user_agent_string)
        self.ua_string = user_agent_string
        self.os = parse_operating_system(**ua_dict["os"])
        self.browser = parse_browser(**ua_dict["user_agent"])
        self.device = parse_device(**ua_dict["device"])

    def __str__(self):
        return "{device} / {os} / {browser}".format(
            device=self.get_device(),
            os=self.get_os(),
            browser=self.get_browser(),
        )

    def __unicode__(self):
        return str(self)

    def _is_android_tablet(self):
        return (
            "Mobile Safari" not in self.ua_string
            and self.browser.family != "Firefox Mobile"
        )

    def _is_blackberry_touch_capable_device(self):
        if "Blackberry 99" in self.device.family:
            return True
        if "Blackberry 95" in self.device.family:
            return True
        return False

    def get_device(self):
        return self.is_pc and "PC" or self.device.family

    def get_os(self):
        return ("%s %s" % (self.os.family, self.os.version_string)).strip()

    def get_browser(self) -> str:
        return (
            "%s %s" % (self.browser.family, self.browser.version_string)
        ).strip()

    @property
    def is_tablet(self):
        if self.device.family in TABLET_DEVICE_FAMILIES:
            return True
        if self.device.brand in TABLET_DEVICE_BRANDS:
            return True
        if self.device.family in MOBILE_DEVICE_FAMILIES:
            return False
        if self.os.family == "Android" and self._is_android_tablet():
            return True
        if self.os.family == "Windows" and self.os.version_string.startswith(
            "RT"
        ):
            return True
        if (
            self.os.family == "Firefox OS"
            and "Mobile" not in self.browser.family
        ):
            return True
        return False

    @property
    def is_mobile(self):
        if self.device.family in MOBILE_DEVICE_FAMILIES:
            return True
        if self.is_tablet or self.is_pc:
            return False
        if self.browser.family in MOBILE_BROWSER_FAMILIES:
            return True
        if self.os.family in ["Android", "Firefox OS", "BlackBerry OS"]:
            return True
        if self.os.family in MOBILE_OS_FAMILIES:
            return True
        if "J2ME" in self.ua_string or "MIDP" in self.ua_string:
            return True
        if "iPhone;" in self.ua_string:
            return True
        if "Googlebot-Mobile" in self.ua_string:
            return True
        if self.device.family == "Spider" and "Mobile" in self.browser.family:
            return True
        # Nokia mobile
        if "NokiaBrowser" in self.ua_string and "Mobile" in self.ua_string:
            return True
        return False

    @property
    def is_touch_capable(self):
        # TODO: detect touch capable Nokia devices
        if self.os.family in TOUCH_CAPABLE_OS_FAMILIES:
            return True
        if self.device.family in TOUCH_CAPABLE_DEVICE_FAMILIES:
            return True
        if self.os.family == "Windows":
            if self.os.version_string.startswith(("RT", "CE")):
                return True
            if (
                self.os.version_string.startswith("8")
                and "Touch" in self.ua_string
            ):
                return True
        if (
            "BlackBerry" in self.os.family
            and self._is_blackberry_touch_capable_device()
        ):
            return True
        return False

    @property
    def is_pc(self):
        if (
            self.device.family in MOBILE_DEVICE_FAMILIES
            or self.device.family in TABLET_DEVICE_FAMILIES
            or self.device.brand in TABLET_DEVICE_BRANDS
        ):
            return False
        # Returns True for "PC" devices (Windows, Mac and Linux)
        if (
            "Windows NT" in self.ua_string
            or self.os.family in PC_OS_FAMILIES
            or self.os.family == "Windows"
            and self.os.version_string == "ME"
        ):
            return True
        if self.os.family == "Mac OS X" and "Silk" not in self.ua_string:
            return True
        # Maemo has 'Linux' and 'X11' in UA, but it is not for PC
        if "Maemo" in self.ua_string:
            return False
        if "Chrome OS" in self.os.family:
            return True
        if "Linux" in self.ua_string and "X11" in self.ua_string:
            return True
        return False

    @property
    def is_bot(self):
        return self.device.family == "Spider"

    @property
    def is_email_client(self):
        return self.browser.family in EMAIL_PROGRAM_FAMILIES
