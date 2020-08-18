from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = "information"


urlpatterns = [
    path("<str:park_type>/overview", views.OverView.as_view(), name="overview"),
    path(
        "<str:park_type>/attractionlist",
        cache_page(60)(views.AttractionList.as_view()),
        name="attractionlist",
    ),
    path(
        "<str:park_type>/<str:attraction_name>/<int:facility_code>/attractiondetail",
        cache_page(60)(views.AttractionDetail.as_view()),
        name="attractiondetail",
    ),
    path(
        "<str:park_type>/favoriteattractionlist",
        cache_page(60)(views.FavoriteAttractionList.as_view()),
        name="favoriteattractionlist",
    ),
    path(
        "<str:park_type>/<str:facility_name>/<int:facility_code>/map",
        cache_page(60 * 60 * 15)(views.AttractionMap.as_view()),
        name="attractionmap",
    ),
    path(
        "<str:park_type>/restaurantlist",
        cache_page(60 * 60 * 15)(views.RestaurantList.as_view()),
        name="restaurantlist",
    ),
    path(
        "<str:park_type>/<str:restaurant_name>/<int:facility_code>/restaurantdetail",
        cache_page(60 * 60 * 15)(views.RestaurantDetail.as_view()),
        name="restaurantdetail",
    ),
    path(
        "<str:park_type>/<str:facility_name>/<int:facility_code>/restaurantmap",
        cache_page(60 * 60 * 15)(views.RestaurantMap.as_view()),
        name="restaurantmap",
    ),
    path(
        "<str:park_type>/shoplist",
        cache_page(60 * 60 * 15)(views.ShopList.as_view()),
        name="shoplist",
    ),
    path(
        "<str:park_type>/<str:shop_name>/<int:facility_code>/shopdetail",
        cache_page(60 * 60 * 15)(views.ShopDetail.as_view()),
        name="shopdetail",
    ),
    path(
        "<str:park_type>/<str:facility_name>/<int:facility_code>/shopmap",
        cache_page(60 * 60 * 15)(views.ShopMap.as_view()),
        name="shopmap",
    ),
]
