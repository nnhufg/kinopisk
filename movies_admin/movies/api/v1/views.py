from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from movies.models import Filmwork
from .serializers import FilmworkSerializer


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'previous': self.page.previous_page_number() if self.page.has_previous() else None,
            'results': data
        })


class MoviesListAPIView(ListAPIView):
    queryset = Filmwork.objects.all()
    serializer_class = FilmworkSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class MoviesDetailAPIView(RetrieveAPIView):
    lookup_field = "id"
    queryset = Filmwork.objects.all() 
    serializer_class = FilmworkSerializer

    def get(self, request, id):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)
