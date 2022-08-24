from django.urls import path
from . import views as place_views

urlpatterns = [
    path('', place_views.PlaceListView.as_view(), name='place_list'),
    path('new_place/', place_views.create_place, name='new_place'),
    path('place/<int:pk>/', place_views.PlaceDetailView.as_view(), name='place_detail'),
    path('place/update/<int:pk>/', place_views.place_update, name='place_update'),
    path('place/delete/<int:pk>/', place_views.PlaceDeleteView.as_view(), name='place_delete'),

    path('delete-reservation/<int:pk>/',  place_views.delete_reservation, name="delete_reservation"),
    path('delete-image/<int:pk>/',  place_views.delete_image, name="delete_image")

]
