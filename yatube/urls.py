from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("posts.urls")), # looks for the front page in posts/urls
    path("admin/", admin.site.urls),
    path('auth/', include('users.urls')), # signing up and auth
    # Checking, if we do not have custom view, then check built-in
    path('auth/', include('django.contrib.auth.urls')),
    path('posts/', include('posts.urls')),


]
