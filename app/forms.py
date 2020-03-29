from django import forms
from tinymce.widgets import TinyMCE

from app.models import Documents


class PostDocumentForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'rows':20,'class': 'form-control'}), required=False)

    class Meta:
        model = Documents
        fields = '__all__'