# -*- coding: utf-8 -*-
from django.urls import path, re_path

from web.views import (
    IndexView,
    MenuView,
    NextTicketView,
    ProcessingView,
    TicketPageView,
)

urlpatterns = [
    path('menu', MenuView.as_view(), name='menu'),
    path('next', NextTicketView.as_view(), name='next_ticket'),
    path('processing', ProcessingView.as_view(), name='processing'),
    re_path('get_ticket/(?P<service>.*)', TicketPageView.as_view(), name='get_ticket'),
    path('welcome', IndexView.as_view(), name='index'),
]
