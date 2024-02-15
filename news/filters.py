import django_filters
from django.forms import DateTimeInput, Select
from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from .models import Post, Category


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='все',
        to_field_name='name'
    )

    post_genre = django_filters.ChoiceFilter(
        field_name='post_genre',
        choices=Post.POST_GENRE,
        label='Post genre',
        empty_label='все',
        widget=Select(attrs={'class': 'form-control'}),
    )

    added_after = DateTimeFilter(
        field_name='post_time',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'category': ['exact'],
            'post_genre': ['exact'],
        }
