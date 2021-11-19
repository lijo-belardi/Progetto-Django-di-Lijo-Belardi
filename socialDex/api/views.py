from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime, timedelta
import hashlib
from .utils import sendTransaction



def posts(request):
    response = []
    posts = Post.objects.filter().order_by('-datetime')
    for post in posts:
        response.append(
            {
                'datetime': post.datetime,
                'content': post.content,
                'user': f"{post.user.first_name} {post.user.last_name}",
                'hash': post.hash,
                'txId': post.txId,
            }
        )
    return JsonResponse(response, safe=False)

# posts of last hour page
def last_hour(request):
    response = []
    # get time now
    this_hour = datetime.now()
    # -1 hour
    one_hour_before = this_hour - timedelta(hours=1)
    # filter posts
    posts = Post.objects.filter(datetime__range=(one_hour_before, this_hour))

    # building Json response
    for post in posts:
        response.append(
            {
                'title': post.title,
                'datetime': post.datetime,
                'content': post.content,
                'user': f"{post.user.first_name} {post.user.last_name}",
                'hash': post.hash,
                'txId': post.txId
            }
        )
    # return Json in the page
    return JsonResponse(response, safe=False)

#for home
class PostListView(ListView):
    model = Post
    template_name = 'base.html'
    context_object_name = 'posts'
    ordering = ['-datetime']
    paginate_by = 5



#for Admin page
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

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = "post_create.html"


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
    #only author can update the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

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
    #only author can update the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/api'
    #only author can delete the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

def statistics(request):
    if request.GET:
        word = request.GET.get('word').capitalize()
        posts = Post.objects.filter(content__contains=word)
        times = len(posts)
        context={
            'times': times,
            'word': word
        }
    else:
        context={}
    return render(request, 'statistics.html', context)

