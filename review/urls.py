from . import views
from django.urls import path


urlpatterns = [
    path('', views.LandingPage.as_view(), name='home'),
    path('directory/', views.ReviewList.as_view(), name='directory'),
    path('<slug:slug>/', views.Review_Single.as_view(), name='single_review'),
]
