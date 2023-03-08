from . import views
from django.urls import path


urlpatterns = [
    path('', views.LandingPage.as_view(), name='home'),
    path('directory/', views.ReviewList.as_view(), name='directory')
]
