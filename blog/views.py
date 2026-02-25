from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Post
from django.views.generic import ListView, DetailView
from django.views import View
from .forms import CommentForm
from django.http import HttpResponseRedirect

# Create your views here.


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class PostDetailView(View):
    template_name = "blog/post-detail.html"

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
        }
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
    
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
        }
        return render(request, self.template_name, context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["stored_posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["stored_posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)
    
    def post(self, request):
        post_id = int(request.POST.get("post_id"))
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        if post_id not in stored_posts:
            stored_posts.append(post_id)

        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")