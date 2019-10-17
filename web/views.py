# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views import View


PROCESSING_TIME = dict([('change_oil', 2), ('inflate_tires', 5), ('make_diagnostics', 30)])
DESCRIPTION = dict([
    ('change_oil', 'Change oil'),
    ('inflate_tires', 'Inflate tires'),
    ('make_diagnostics', 'Make diagnostics'),
])
AVERAGE_PROCESSING_TIME = 1

current_number = None
next_number = 1


@dataclass(order=True)
class Ticket:
    service: str
    number: int


queues_size: Dict[str, List[int]] = {key: [] for key in DESCRIPTION.keys()}


############################################################
## Handlers
############################################################

class IndexView(View):
    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'web/index.html')


class MenuView(View):
    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'web/menu.html', context={'description': DESCRIPTION})


class NextTicketView(View):
    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        global current_number
        return render(request, 'web/next_ticket.html', context={'next_ticket': current_number})


class ProcessingView(View):
    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request, 'web/processing.html',
            context={
                'change_oil_left': len(queues_size['change_oil']),
                'inflate_tires_left': len(queues_size['inflate_tires']),
                'make_diagnostics_left': len(queues_size['make_diagnostics']),
            }
        )

    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        global current_number
        service = self.__next_service()

        if service:
            current_number = queues_size[service].pop(0)
        else:
            current_number = None
        return redirect(reverse('processing'))

    def __next_service(self) -> str:
        if queues_size['change_oil']:
            return 'change_oil'
        elif queues_size['inflate_tires']:
            return 'inflate_tires'
        elif queues_size['make_diagnostics']:
            return 'make_diagnostics'
        return ''


class TicketPageView(View):
    def get(self, request: WSGIRequest, service: str, *args, **kwargs) -> HttpResponse:
        global next_number
        service = service.strip('/')
        ticket = Ticket(service, next_number)
        time_to_wait = len(queues_size['change_oil']) * PROCESSING_TIME['change_oil']
        if service != 'change_oil':
            time_to_wait += len(queues_size['inflate_tires']) * PROCESSING_TIME['inflate_tires']
        if service == 'make_diagnostics':
            time_to_wait += (
                len(queues_size['make_diagnostics']) * PROCESSING_TIME['make_diagnostics']
            )
        queues_size[service].append(next_number)
        next_number += 1
        return render(
            request, 'web/ticket.html',
            context={
                'ticket': ticket,
                'time_to_wait': time_to_wait,
                'current_time': datetime.now(),
            }
        )
