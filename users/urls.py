from django.urls import path

from . import views

urlpatterns = [
    # path for signing up a new user
    # full path is auth/signup, but auth is already in the root urls (yatube)
    path('signup/', views.SignUpView.as_view(), name='signup')
]
