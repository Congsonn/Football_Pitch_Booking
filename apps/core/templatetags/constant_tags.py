from django import template
from django.shortcuts import resolve_url

register = template.Library()

NAVBAR_LINKS = [
    {"url": "/", "label": "Trang chủ"},
    {"url": resolve_url("pitches"), "label": "Sân bóng"},
    {"url": "/about_us", "label": "Về chúng tôi"},
    {"url": "#", "label": "Liên hệ"},
]

CONFIG = {
    "web_name": "Sanbongssc",
    "description": "Sanbongssc Description",
    "shortcute_icon": "/static/imgs/logo.jpg",
    "copyright": "Sanbongssc. All Rights Reserved",
}


@register.simple_tag
def get_navbar_links():
    return NAVBAR_LINKS


@register.simple_tag
def get_config_settings():
    return CONFIG
