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
        "<str:park_type>/<str:attraction_name>/<int:facility_code>/attractiondetail",
        views.AttractionDetail.as_view(),
        name="attractiondetail",
    ),
    path(
        "<str:park_type>/<str:facility_name>/<int:facility_code>/map",
        views.AttractionMap.as_view(),
        name="attractionmap",
    ),
    path(
        "<str:park_type>/restaurantlist",
        views.RestaurantList.as_view(),
        name="restaurantlist",
    ),
    path(
        "<str:park_type>/<str:restaurant_name>/<int:facility_code>/restaurantdetail",
        views.RestaurantDetail.as_view(),
        name="restaurantdetail",
    ),
    path(
        "<str:park_type>/<str:facility_name>/<int:facility_code>/restaurantmap",
        views.RestaurantMap.as_view(),
        name="restaurantmap",
    ),
    path("<str:park_type>/shoplist", views.ShopList.as_view(), name="shoplist"),
    path(
        "<str:park_type>/<str:shop_name>/<int:facility_code>/shopdetail",
        views.ShopDetail.as_view(),
        name="shopdetail",
    ),
    path(
        "<str:park_type>/<str:facility_name>/<int:facility_code>/shopmap",
        views.ShopMap.as_view(),
        name="shopmap",
    ),
]
