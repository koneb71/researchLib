import logging

from django.conf.global_settings import LOGOUT_REDIRECT_URL
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse

from app.forms import PostDocumentForm
from app.models import Documents


def logout_user(request):
    logout(request)
    return redirect('/')


def index(request):
    papers = Documents.objects.filter(is_published=True)

    return render(request, 'index.html', {'papers': papers})


def post_research(request):
    form = PostDocumentForm(request.POST, request.FILES)

    if request.method == 'POST' and form.is_valid():
        form.save(commit=True)
        return redirect(reverse('index'))
    return render(request, 'post.html')
