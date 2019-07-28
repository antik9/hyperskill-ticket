# -*- coding: utf-8 -*-
from django.urls import path, re_path

from web.views import get_index_page, get_main_page, get_ticket_page, process_next_ticket

urlpatterns = [
    path('main', get_main_page, name='main'),
    path('processing', process_next_ticket, name='processing'),
    re_path('ticket/(?P<level>\d)', get_ticket_page, name='get_ticket'),
    path('', get_index_page, name='index'),
]
