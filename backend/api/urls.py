from django.urls import path

from . import views

urlpatterns = [
    path("newton_fractal/", views.newton_fractal, name="newton_fractal"),
]
