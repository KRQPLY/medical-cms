from django import forms
from client.models import Page, Slider

class PageForm(forms.ModelForm):
    class Meta:
        fields='__all__'
        exclude = ('created_by','modified_by')

class ComponentForm(forms.ModelForm):
    class Meta:
        fields='__all__'
        widgets = {
            'page': forms.CheckboxSelectMultiple()
        }