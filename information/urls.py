from django.urls import path
from . import views

app_name = "information"


urlpatterns = [
    path("<str:park_type>/", views.Home.as_view(), name="home"),
    path(
        "<str:park_type>/<str:attraction_name>/<int:facility_code>/detail",
        views.Detail.as_view(),
        name="detail",
    ),
]
