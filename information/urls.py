from django.urls import path
from . import views

app_name = "information"


urlpatterns = [
    path("<str:park_type>/overview", views.OverView.as_view(), name="overview"),
    path(
        "<str:park_type>/attractionlist",
        views.AttractionList.as_view(),
        name="attractionlist",
    ),
    path(
        "<str:park_type>/restaurantlist",
        views.RestaurantList.as_view(),
        name="restaurantlist",
    ),
    path(
        "<str:park_type>/<str:attraction_name>/<int:facility_code>/detail",
        views.Detail.as_view(),
        name="detail",
    ),
    path(
        "<str:park_type>/<str:attraction_name>/<int:facility_code>/map",
        views.Map.as_view(),
        name="map",
    ),
]
