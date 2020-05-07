from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        group = forms.ChoiceField(required=False)
        fields = ('group', 'text')
