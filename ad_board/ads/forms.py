from django.forms import *
from .models import Ad, Category
from tinymce import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class AdForm(ModelForm):
    category = ModelChoiceField(queryset=Category.objects.all())
    content = CharField(widget=TinyMCEWidget())

    class Meta:
        model = Ad
        fields = ['title', 'category', 'content']