from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ( 
  ListView,
  DetailView,
  CreateView,
  UpdateView,
  DeleteView
) 
from .models import Post


class PostListView(ListView):
  model = Post
  context_object_name = 'posts'
  ordering = ['-date_posted']
  template_name = 'blog/home.html'  #<app>/<model>_<viewtype>.html
  paginate_by = 4

class UserPostListView(ListView):
  model = Post
  context_object_name = 'posts'
  template_name = 'blog/user_posts.html'  #<app>/<model>_<viewtype>.html
  paginate_by = 5
  
  def get_queryset(self):
    user = get_object_or_404(User, username=self.kwargs.get('username'))
    return Post.objects.filter(author=user).order_by('-date_posted')
    
  
class PostDetailView(DetailView):
  model = Post
  
class PostCreateView(SuccessMessageMixin ,LoginRequiredMixin, CreateView):
  model = Post
  success_message = "Your Post is Created!"
  fields = ['title', 'description', 'content']
  
  
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
  model = Post
  fields = ['title', 'description', 'content']
  success_message = "Your post is Updated!"
  
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
  
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):
  model = Post
  
  def test_func(self):
    post = self.get_object()
    if self.request.user == post.author:
      return True
    return False
  success_url = '/blog'  
    
def about(request):
  return render(request, 'blog/about.html')
  
def home(request):
  return render(request, 'blog/startpage.html')