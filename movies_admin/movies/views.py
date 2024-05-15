from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    CompoundSearchFilterBackend,
)
from .documents import *
from .serializers import FilmworkELSSerializer


class FilmworkDocumentView(DocumentViewSet):
    document = FilmWorkDocument
    serializer_class = FilmworkELSSerializer
    lookup_field = 'title'
    fielddata=True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]
   
    search_fields = (
        'title',
        'description',
    )
    multi_match_search_fields = (
       'title',
        'description',
    )
    filter_fields = {
       'title' : 'title',
        'description' : 'description',
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ( 'id'  ,)
