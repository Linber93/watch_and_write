from django.shortcuts import render
from django.views import generic
from .models import Review
from .forms import CommentForm


class ReviewList(generic.ListView):
    """
    Review directory view
    """
    model = Review
    template_name = 'directory.html'
    paginate_by = 6
    queryset = Review.objects.filter(status=1).order_by('-created_on')


class LandingPage(generic.ListView):
    """
    landing page view
    """
    model = Review
    template_name = 'index.html'
    paginate_by = 3
    queryset = Review.objects.filter(status=1).order_by('created_on')
