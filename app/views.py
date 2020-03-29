import logging
import uuid

from django.conf.global_settings import LOGOUT_REDIRECT_URL
from django.contrib.auth import logout, get_user
from django.shortcuts import render, redirect, get_object_or_404
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
        form.save(commit=False)
        form.created_by = request.user.pk
        form.save()
        return redirect(reverse('index'))
    return render(request, 'post.html', {'form': form})

def view_research(request, id):
    item = get_object_or_404(Documents, pk=id)
    return render(request, 'view.html', {'item': item})