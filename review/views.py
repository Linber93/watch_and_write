from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Review
from .forms import CommentForm


class ReviewList(generic.ListView):
    """
    Review directory view
    """
    model = Review
    template_name = 'directory.html'
    paginate_by = 6
    queryset = Review.objects.filter(status=1).filter(review_approved=True).order_by('-created_on')


class LandingPage(generic.ListView):
    """
    landing page view
    """
    model = Review
    template_name = 'index.html'
    paginate_by = 3
    queryset = Review.objects.filter(status=1).filter(review_approved=True).order_by('created_on')


class Review_Single(View):
    """
    View for displaying information about a single NGO
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Get method for retrieving a particular record
        """
        queryset = Review.objects.filter(status=1)
        reviews = get_object_or_404(queryset, slug=slug)
        comments = reviews.comments.filter(comment_approved=True).order_by("-created_on")
        liked = False
        if reviews.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'single-review.html',
            {
                'reviews': reviews,
                'comments': comments,
                'liked': liked,
                'comment_form': CommentForm()
            }
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Review.objects.filter(status=1)
        reviews = get_object_or_404(queryset, slug=slug)
        comments = reviews.comments.filter(comment_approved=True).order_by("-created_on")
        liked = False
        if reviews.likes.filter(id=self.request.user.id).exists():
            liked = True

        template_name = 'single-review.html'
        context = {
            'reviews': reviews
        }

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.reviews = reviews
            comment.review_id = reviews.id
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "single-review.html",
            {
                "reviews": reviews,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )
