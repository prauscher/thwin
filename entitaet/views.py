from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from .login import require_login


@require_login
def index(request):
    return HttpResponse("Hello world: {}".format(request.session["person_id"]))
