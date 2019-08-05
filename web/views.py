# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from heapq import heappush, heappop, nsmallest
from typing import List, Tuple, Dict

from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponse
from django.core.handlers.wsgi import WSGIRequest

URGENCY_LEVEL = dict([(1, 'Urgent'), (2, 'Normal'), (3, 'Lazy')])
AVERAGE_PROCESSING_TIME = 1
next_number = 1
processed = 0
revoked = 0

@dataclass(order=True)
class Ticket:
    level: int
    message: str
    number: int


ticket_queue: List[Ticket] = []
queues_size: Dict[str, int] = {key: 0 for key in URGENCY_LEVEL.keys()}

############################################################
## Handlers
############################################################

def get_index_page(request: WSGIRequest, *args, **kwargs) -> HttpResponse:
    return render(request, 'web/index.html')


def get_main_page(request: WSGIRequest, *args, **kwargs) -> HttpResponse:
    global ticket_queue
    if ticket_queue:
        next_ticket = nsmallest(1, ticket_queue)[0]
    return render(request, 'web/index2.html', context={'levels': URGENCY_LEVEL})


def get_ticket_page(request: WSGIRequest, level: int, *args, **kwargs) -> HttpResponse:
    global next_number, queues_size, ticket_queue
    level = int(level)
    ticket = Ticket(level, 'Some task', next_number)
    heappush(ticket_queue, ticket)
    queues_size[level] += 1
    next_number += 1
    clients_before = sum(queues_size[l] for l in queues_size if l <= level) - 1
    return render(
        request, 'web/ticket.html',
        context={
            'ticket': ticket,
            'time_to_wait': clients_before * AVERAGE_PROCESSING_TIME,
            'current_time': datetime.now(),
        }
    )


def process_next_ticket(request: WSGIRequest, *args, **kwargs) -> HttpResponse:
    global queues_size, ticket_queue, processed, revoked

    ticket = nsmallest(1, ticket_queue)[0] if ticket_queue else None
    urgency = None
    if ticket:
        urgency = URGENCY_LEVEL[ticket.level]

    if request.method == 'POST':
        if request.POST.get('action') == 'process':
            processed += 1
        elif request.POST.get('action') == 'revoke':
            revoked += 1
        heappop(ticket_queue) if ticket_queue else None
        queues_size[ticket.level] -= 1
        return redirect(reverse('processing'))

    return render(
        request, 'web/processing.html',
        context={
            'ticket': ticket, 'urgency': urgency,
            'processed': processed, 'revoked': revoked
        }
    )
