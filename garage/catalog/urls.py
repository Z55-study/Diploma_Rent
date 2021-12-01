from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bikes/', views.BikeListView.as_view(), name='bikes'),
    path('bike/<int:pk>', views.BikeDetailView.as_view(), name='bike-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybikes/', views.LoanedBikesByUserListView.as_view(), name='my-borrowed'),
    path(r'borrowed/', views.LoanedBikesAllListView.as_view(), name='all-borrowed'),  # Added for challenge
    path('bike/<uuid:pk>/renew/', views.renew_bike_librarian, name='renew-bike-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('bike/create/', views.BikeCreate.as_view(), name='bike-create'),
    path('bike/<int:pk>/update/', views.BikeUpdate.as_view(), name='bike-update'),
    path('bike/<int:pk>/delete/', views.BikeDelete.as_view(), name='bike-delete'),
]
