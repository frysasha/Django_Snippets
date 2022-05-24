from django.forms import ModelForm, TextInput, Textarea
from MainApp.models import Snippet


class SnippetForm(ModelForm):
   class Meta:
       model = Snippet
       fields = ['name', 'lang', 'code']
       widgets = {
           'name': TextInput({"class":"form-control form-control-lg", 'placeholder': 'Название сниппета'}),
       }