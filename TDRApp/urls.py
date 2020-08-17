"""TDRApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.urls import path, include
from . import views


urlpatterns = [
    path("", cache_page(60 * 15)(views.Top.as_view()), name="top"),
    path("error", views.Error.as_view(), name="error"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # [追加]
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("information.urls")),
    path("", include("standbytime.urls")),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns

