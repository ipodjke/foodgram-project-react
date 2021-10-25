from django.conf import settings
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe
from rest_framework.filters import BaseFilterBackend, SearchFilter
from tags.models import Tag


class DoubleSearchBackend(SearchFilter):
    """
    Бекенд для фильтрации с выводом в заданой последовательности.

    Поддерживает примущества базавого фильтра, но выводит
    результаты в последовательности указанной в search_fields
    """
    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in search_fields
        ]

        filtered_queryset = []
        for search_term in search_terms:
            for orm_lookup in orm_lookups:
                ingredients = (queryset.filter(
                    **{orm_lookup: search_term}
                ))
                for ingredient in ingredients:
                    if ingredient not in filtered_queryset:
                        filtered_queryset.append(ingredient)

        return filtered_queryset


class IsFavoritedFilterBackend(BaseFilterBackend):
    """
    Фильтр для вывода избраных рецептов пользователя.

    Подерживает установленную пагинацию с ее фильтрами.
    Приорететней над базовыми drf фильтрами.
    """
    def filter_queryset(self, request, queryset, view):
        path_name = settings.PATH_PARAM_NAMES.get('favorited')

        if (not request.user.is_anonymous
                and request.query_params.get(path_name, '0') == '1'):
            return request.user.marked_recipes.fovorited_recipe.all()

        return queryset


class IsDownloadFilterBackend(BaseFilterBackend):
    """
    Фильтр для вывода рецептов из корзины пользователя.

    Подерживает установленную пагинацию с ее фильтрами.
    Приорететней над базовыми drf фильтрами.
    """
    def filter_queryset(self, request, queryset, view):
        path_name = settings.PATH_PARAM_NAMES.get('shopping_cart')

        if (not request.user.is_anonymous
                and request.query_params.get(path_name, '0') == '1'):
            return request.user.marked_recipes.recipe_for_download.all()

        return queryset


class RecipeFilterSet(FilterSet):
    """
    Фильтерсет для переопределения поведения фильтрации
    поля slug.

    Переопределено поведение фильтрации с поля id на slug при
    фильтрации по tags.
    При фильтрации по author фильтрация идет по id.
    """
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        to_field_name='slug',
        field_name='tags__slug'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
