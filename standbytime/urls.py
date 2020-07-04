from django.urls import path
from . import views

app_name = "standbytime"

urlpatterns = [
    path(
        "<str:park_type>/<str:attraction_name>/<int:facility_code>/standbytime",
        views.standbytime.as_view(),
        name="standbytime",
    ),
]
