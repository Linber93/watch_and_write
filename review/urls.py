from . import views
from django.urls import path


urlpatterns = [
    path('', views.LandingPage.as_view(), name='home'),
    path('directory/', views.ReviewList.as_view(), name='directory'),
    path('create-review/', views.CreateReview.as_view(), name='create_review'),
    path('reviews/edit/<slug:slug>/', views.EditReview.as_view(), name='edit_review'),
    path('reviews/<slug:slug>/remove', views.DeleteReview.as_view(), name='delete_review'),
    path('reviews/search-results', views.SearchResults.as_view(), name='search_results'),
    path('<slug:slug>/', views.Review_Single.as_view(), name='single_review'),

]
