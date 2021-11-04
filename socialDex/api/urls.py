'''API URL'''

from django.urls import path
from .views import PostListView, AdminPageView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView

app_name = 'api'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('only-admin/', AdminPageView.as_view(), name='admin'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),

]