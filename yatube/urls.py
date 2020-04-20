from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("posts.urls")), # importing rules from posts app
    path("admin/", admin.site.urls),
]   # importing rules from admin app
