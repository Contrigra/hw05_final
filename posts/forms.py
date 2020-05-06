from django import forms
from .models import Post, Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        GROUP_CHOICES = Group.objects.values_list('id', 'title')
        group = forms.ChoiceField(required=False, choices=GROUP_CHOICES)
        fields = ('group', 'text')
