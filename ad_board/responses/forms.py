from django.forms import *
from .models import Response


class ResponseForm(ModelForm):

    class Meta:
        model = Response
        fields = ['content']
