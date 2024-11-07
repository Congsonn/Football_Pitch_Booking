from django.core.paginator import Paginator


ITEM_PER_PAGE = 12


def format_number_with_commas(value):
    value_str = "{:,}".format(int(value))
    return value_str


def format_datetime_vn(value):
    day = value.strftime("%d")
    month = f"Tháng {value.month}"
    year = value.strftime("%Y")
    time = value.strftime("%H:%M")
    return f"{time}, {day} {month} {year}"


def get_paginator(request, queryset, item_per_page=ITEM_PER_PAGE):
    if queryset.count() < item_per_page:
        return queryset

    p = Paginator(queryset, item_per_page)
    page = request.GET.get("page")
    return p.get_page(page)
