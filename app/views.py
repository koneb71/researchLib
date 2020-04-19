import logging

from django.contrib.auth import logout, get_user
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from six import BytesIO

from app.forms import PostDocumentForm
from app.models import Documents, PublicationType, Departments, Colleges, Images
from app.pdf_image_extractor import extract_images


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
        doc = form.save()

        document = Documents.objects.filter(pk=doc.pk).first()
        if document:
            # for name in all_keywords:
            #     text, _ = Keywords.objects.get_or_create(text=name)
            #     document.keywords.add(text)
            #     document.save()
            pdf_images = extract_images(document.file.path)

            for index, img in enumerate(pdf_images):
                try:
                    output = BytesIO()
                    img.save(output, format='JPEG')
                    output.seek(0)
                    data = InMemoryUploadedFile(output, 'ImageField', "%s-%s.jpg" % (document.title, index),
                                                'image/jpeg',
                                                output.__sizeof__(), None)
                    image_form = Images(image=data)
                    img = image_form.save()
                    document.images.add(img)
                    document.save()
                except Exception as e:
                    logging.error(e)
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
