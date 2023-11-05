from django import forms
from ckeditor.widgets import CKEditorWidget

class MyModelForm(forms.ModelForm):
    class Meta:
        fields = '__all__'

    description = forms.CharField(widget=CKEditorWidget())