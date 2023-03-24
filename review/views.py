from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView
from django.views import generic, View
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from .models import Review
from .forms import CommentForm, ReviewForm


class ReviewList(generic.ListView):
    """
    Review directory view
    """
    model = Review
    template_name = 'directory.html'
    paginate_by = 6
    queryset = Review.objects.filter(review_approved=True).order_by('-created_on')


class LandingPage(generic.ListView):
    """
    landing page view
    """
    model = Review
    template_name = 'index.html'
    paginate_by = 3
    queryset = Review.objects.filter(review_approved=True).order_by('created_on')


class ReviewSingle(View):
    """
    View for displaying information about a single review
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Get method for retrieving a particular record
        """
        queryset = Review.objects
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
        if not request.user.is_authenticated:
            return redirect(reverse('login'))

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


class CreateReview(generic.CreateView, LoginRequiredMixin):
    """
    View to Create a review
    """
    model = Review
    form_class = ReviewForm
    template_name = 'create-review.html'

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.email = request.user.email
            review.author = request.user
            review.slug = f'{review.title}_{review.author}'
            review.save()

            context = {
                "review_form": review_form,
                "reviewed": True,
            }
        else:
            context = {
                "review_form": review_form,
                "reviewed": False,
                "failure": True,
            }

        return render(request, self.template_name, context)


class EditReview(generic.UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    """
    View to Edit a review
    """
    model = Review
    template_name = 'edit-review.html'
    form_class = ReviewForm

    def get(self, request, *args, **kwargs):
        """
        Retrieves the review that is being updated
        """
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles resubmission of the edited review,
        also sets review to being not approved
        """
        self.object = self.get_object()
        user_update_form = self.get_form()
        if user_update_form.is_valid():
            review = user_update_form.save(commit=False)
            review.email = request.user.email
            review.author = request.user
            review.slug = slugify(review.title)
            review.review_approved = False
            return self.form_valid(user_update_form)
        else:
            return self.form_invalid(user_update_form)

    def form_valid(self, user_update_form):
        """
        Saves the updated review to the database
        Then renders the edit_review page with a custom context
        The context is used to display a success message
        """
        self.object = user_update_form.save()
        template_name = self.template_name
        context = {
            "update_review_form": ReviewForm(),
            "updated": True
        }
        return render(self.request, template_name, context)

    def form_invalid(self, user_update_form):
        """
        Handles invalid forms, such as if the user has already reviewed that movie of that the form wasn't filled in completely
        """
        template_name = self.template_name
        context = {
            "update_review_form": user_update_form,
            "updated": False,
            "failure": True
        }
        return render(self.request, template_name, context)

    def test_func(self):
        """Test that logged in user is post author"""
        post = self.get_object()
        if self.request.user == review.author:
            return True
        return False


class DeleteReview(generic.DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    """
    The view used for deleting a review on the front-end
    Does not use a get or post method
    The generic DeleteView handles all deletion functionality
    Upon success, redirects to the landing page
    """
    model = Review
    template_name = 'delete-review.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        """Test that logged in user is post author"""
        post = self.get_object()
        if self.request.user == review.author:
            return True
        return False


class SearchResults(generic.ListView):
    """
    The view for rendering the search results page.
    assigned three variables that set the model, template and pagination
    """
    model = Review
    template_name = 'search_results.html'
    paginate_by = 3

    def querystring(self):
        """
        querystring method
        Required for retaining the same queryset across all pagination pages
        """
        querystring = self.request.GET.copy()
        querystring.pop(self.page_kwarg, None)
        encoded_querystring = querystring.urlencode()
        return encoded_querystring

    def get_queryset(self):
        """
        get_queryset method
        Constructs a queryset using Q methods
        Returns an object_list for use within the template
        """
        query = self.request.GET.get('search')

        if query is not None:
            object_list = Review.objects.filter(
                Q(title__icontains=query) |
                Q(author__username__icontains=query) |
                Q(director__icontains=query) |
                Q(actors__icontains=query)
                ).filter(review_approved=True)
        else:
            object_list = Review.objects.none()

        return object_list
