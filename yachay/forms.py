from django import forms
from django.db.models import Model
from django.forms import Form, ModelForm, TextInput, fields, widgets
from yachay.models import *


class TagForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'ejemplo: filosofía',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class LineForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Line
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'ejemplo: filosofía',
                }
            ),
        }

class NoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Note
        fields = ['content', 'zettel_id', 'category', 'resource']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe el contenido aquí'}),
            'zettel_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID único'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoría'}),
            'resource': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class NoteTagForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['tag'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = NoteTag
        fields = ['tag']
        widgets = {
            'tag': forms.Select(attrs={'class': 'form-control'}),
        }

