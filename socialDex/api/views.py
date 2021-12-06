from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime, timedelta
import hashlib
from .utils import sendTransaction

#JSON for all posts
def posts(request):
    response = []
    posts = Post.objects.filter().order_by('-datetime')
    for post in posts:
        response.append(
            {
                'datetime': f"{post.datetime}",
                'user': f"{post.user}",
                'title': f"{post.title}",
                'content': f"{post.content}",
                'hash': f"{post.hash}",
                'txId': f"{post.txId}",
            }
        )
    return JsonResponse(response, safe=False, json_dumps_params={'indent': 3})

# JSON for posts of the last hour
def last_hour(request):
    response = []
    # get time now
    this_hour = datetime.now()
    # -1 hour
    one_hour_before = this_hour - timedelta(hours=1)
    # filter posts
    posts = Post.objects.filter(datetime__range=(one_hour_before, this_hour)).order_by('-datetime')

    # Building JSON response
    for post in posts:
        response.append(
            {
                'datetime': f"{post.datetime}",
                'user': f"{post.user}",
                'title': f"{post.title}",
                'content': f"{post.content}",
                'hash': f"{post.hash}",
                'txId': f"{post.txId}",
            }
        )
    # return JSON in the page
    return JsonResponse(response, safe=False, json_dumps_params={'indent': 3})

# HOME View
class PostListView(ListView):
    model = Post
    template_name = 'base.html'
    context_object_name = 'posts'
    ordering = ['-datetime']
    paginate_by = 5

#Admin page class
class AdminPageView(ListView):
    model = Post
    template_name = "admin.html"
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the user_posts
        context['user_posts'] = User.objects.annotate(total_posts=Count('post'))
        return context

    def test_func(self):
        return self.request.user.is_superuser

#Post create class
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = "post_create.html"

    # Function for word 'hack' (title and content)
    def form_valid(self, form):
        forbidden_word = "hack"
        if not forbidden_word in self.request.POST['content']:
            if not forbidden_word in self.request.POST['title']:
                form.instance.user = self.request.user
                form.instance.hash = hashlib.sha256(((self.request.POST['content'])).encode('utf-8')).hexdigest()
                form.instance.txId = sendTransaction(form.instance.hash)
                return super().form_valid(form)
            else:
                return render(self.request, 'post_form_forbidden.html', {})
        else:
            return render(self.request, 'post_form_forbidden.html', {})

#Post detail class
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def form_valid(self, form):
        forbiddenword = "hack"
        if not forbiddenword in self.request.POST['content']:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            return render(self.request, 'post_form_forbidden.html', {})

    # Only author can update the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

# Post update class
class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_form.html'

    def form_valid(self, form):
        forbiddenword = "hack"
        if not forbiddenword in self.request.POST['content']:
            if not forbiddenword in self.request.POST['title']:
                form.instance.user = self.request.user
                form.instance.hash = hashlib.sha256(((self.request.POST['content'])).encode('utf-8')).hexdigest()
                form.instance.txId = sendTransaction(form.instance.hash)
                return super().form_valid(form)
            else:
                return render(self.request, 'post_form_forbidden.html', {})
        else:
            return render(self.request, 'post_form_forbidden.html', {})

    # Only author can update the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

# Post delete class
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/api'

    # Only author can delete the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

# Statistics function
def statistics(request):
    if request.GET:
        word = request.GET.get('word').capitalize()
        posts = Post.objects.filter(content__contains=word)
        times = len(posts)
        context = {
            'times': times,
            'word': word
        }
    else:
        context = {}
    return render(request, 'statistics.html', context)

