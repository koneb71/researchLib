from django.forms import ModelForm

from app.models import Documents


class PostDocumentForm(ModelForm):
    class Meta:
        model = Documents
        fields = '__all__'