from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Case, Value, When
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, PersonFilmWork


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        queryset = FilmWork.objects.values('id', 'title', 'description', 'creation_date', 'rating', 'type').annotate(
            actors=ArrayAgg(
                Case(When(personfilmwork__role=PersonFilmWork.RoleType.ACTOR, then='personfilmwork__person__full_name'),
                     default=Value([])), distinct=True),
            directors=ArrayAgg(Case(
                When(personfilmwork__role=PersonFilmWork.RoleType.DIRECTOR, then='personfilmwork__person__full_name'),
                default=Value([])), distinct=True),
            writers=ArrayAgg(Case(
                When(personfilmwork__role=PersonFilmWork.RoleType.WRITER, then='personfilmwork__person__full_name'),
                default=Value([])), distinct=True),
            genres=ArrayAgg('genres__name', distinct=True),
        )

        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(self.get_queryset(), self.paginate_by)

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.object

