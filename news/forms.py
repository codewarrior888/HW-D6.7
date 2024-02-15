from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'post_title',
            'post_text',
            'category',
            ]

    def clean(self):
        cleaned_data = super().clean()
        post_title = cleaned_data.get("post_title")
        if post_title is not None and len(post_title) < 10:
            raise ValidationError({
                "post_title": "Название не может быть менее 10 символа.",
            })

        post_text = cleaned_data.get("post_text")
        if post_text == post_title:
            raise ValidationError({
                "Описание не должно быть идентично названию.",
            })

        return cleaned_data

    def clean_name(self):
        post_title = self.cleaned_data["post_title"]
        if post_title[0].islower():
            raise ValidationError({
                "Название должно начинаться с заглавной буквы",
            })
        return post_title
