from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # flatpages
    path('about/', include('django.contrib.flatpages.urls')),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("", include("posts.urls")),
]

urlpatterns += [path('about-author/', views.flatpage,
                     {'url': '/about-author/'}, name='About_the_author'),
                path('about-spec/', views.flatpage,
                     {'url': '/about-spec/'}, name='Technologies_used')
                ]
