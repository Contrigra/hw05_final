from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    # flatpages
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='About_the_author'),
    path('about-spec/', views.flatpage,
         {'url': '/about-spec/'}, name='Technologies_used'),
    # posts app
    path("", include("posts.urls")),
]
