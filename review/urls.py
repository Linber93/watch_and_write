from . import views
from django.urls import path


urlpatterns = [
    path('', views.LandingPage.as_view(), name='home'),
    path('directory/', views.ReviewList.as_view(), name='directory'),
    path('create-review/', views.CreateReview.as_view(), name='create_review'),
    path('<slug:slug>/', views.Review_Single.as_view(), name='single_review'),
]
