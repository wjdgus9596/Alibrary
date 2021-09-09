from django import forms
from pybo.models import User, UploadFileModel


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'subject': 'Name',
            'content': 'Content',
        }

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel
        fields = ('title', 'file',)