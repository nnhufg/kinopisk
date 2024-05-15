from django.urls import path
from movies.api.v1.views import MoviesDetailAPIView, MoviesListAPIView

urlpatterns = [
    path('movies/', MoviesListAPIView.as_view(), name='movies-list-api'),
    path('movies/<uuid:id>/', MoviesDetailAPIView.as_view(), name='movie-detail-api'),
]