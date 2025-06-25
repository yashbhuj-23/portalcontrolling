from django import forms
from .models import ResumeRequest

class ResumeRequestForm(forms.ModelForm):
    class Meta:
        model = ResumeRequest
        # fields = ['name', 'contact', 'education', 'skills']
        fields = ['firstname', 'contact', 'education', 'skills']

        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'education': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
