import uuid

from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from PIL import Image as Img
from io import BytesIO

from tinymce.models import HTMLField
from versatileimagefield.fields import VersatileImageField, PPOIField
from uuid_upload_path import upload_to

from app.validators import validate_file_extension



def compress_image(image_object, image_quality=settings.IMAGE_QUALITY):
    """
    To compress any image file.
    :param image_object: Image object to be compress
    :param image_quality: quality of image after compression
    :return: Compressed image object
    """
    image_object.open()
    img = Img.open(BytesIO(image_object.read()))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    basewidth = settings.IMAGE_BASE_WIDTH
    if basewidth >= image_object.width:
        img.thumbnail((image_object.width, image_object.height), Img.ANTIALIAS)
    else:
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img.thumbnail((basewidth, hsize), Img.ANTIALIAS)

    # print("%d , %d " % (img.size[0],img.size[1]))
    output = BytesIO()
    img.save(output, format='JPEG', quality=image_quality)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image_object.name.split('.')[0],
                                'image/jpeg',
                                output.__sizeof__(), None)


class ImageMixin(models.Model):
    '''
    An abstract base class model that provides a VersatileImageField Image with POI
    '''

    image = VersatileImageField(upload_to=upload_to, blank=True, null=True, ppoi_field='image_poi',
                                verbose_name="image")
    image_poi = PPOIField(verbose_name="image's Point of Interest", blank=True, null=True)  # point of interest

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super(ImageMixin, self).save(*args, **kwargs)


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Colleges(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'

    def __str__(self):
        return self.name


class Departments(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    college = models.ForeignKey(Colleges, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return "%s - %s" % (self.college.name, self.name)


class Courses(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return "%s - %s" % (self.department.name, self.name)


class Authors(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Images(BaseModel, ImageMixin):
    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.image.name


class Files(BaseModel):
    name = models.CharField(max_length=255, blank=True)
    path = models.FileField(upload_to=upload_to, null=True, blank=True)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return self.name


class Documents(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    short_description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    abstract = HTMLField(null=True, blank=True)
    file = models.FileField(upload_to=upload_to, validators=[validate_file_extension], null=True, blank=True)
    authors = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey(Departments, on_delete=models.DO_NOTHING, null=True, blank=True)
    images = models.ManyToManyField(Images, null=True, blank=True)
    additional_files = models.ManyToManyField(Files, null=True, blank=True)
    tags = models.ManyToManyField('Tags', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.title


class Tags(BaseModel):
    text = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.text
