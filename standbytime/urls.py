from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = "standbytime"

urlpatterns = [
    path(
        "<str:park_type>/<str:attraction_name>/<int:facility_code>/standbytime",
        cache_page(60 * 15)(views.standbytime.as_view()),
        name="standbytime",
    ),
]
