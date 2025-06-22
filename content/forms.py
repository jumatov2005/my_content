from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ismingiz',
                'class': 'form-control',
                'style': 'background-color:#2c2c2c; color:#fff; border:none; border-radius:8px; padding:10px; margin-bottom:10px;'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Fikringizni yozib qoldiring...',
                'rows': 4,
                'class': 'form-control',
                'style': 'background-color:#2c2c2c; color:#fff; border:none; border-radius:8px; padding:10px;'
            }),
        }
