from django.contrib.auth import logout, get_user
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from app.forms import PostDocumentForm
from app.models import Documents, PublicationType, Departments, Colleges


def logout_user(request):
    logout(request)
    return redirect('/')


def index(request):
    papers = Documents.objects.filter()
    colleges = Colleges.objects.filter()
    departments = Departments.objects.filter()
    return render(request, 'index.html', {'papers': papers, 'colleges': colleges, 'departments': departments})


def post_research(request):
    form = PostDocumentForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('index'))

    publication_types = PublicationType.objects.all()
    return render(request, 'post.html', {'form': form, 'publication_types': publication_types})


def view_research(request, id):
    item = get_object_or_404(Documents, pk=id)
    return render(request, 'view.html', {'item': item})


def send_pdf(request, id):
    item = get_object_or_404(Documents, pk=id)
    with open(item.file.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        return response
