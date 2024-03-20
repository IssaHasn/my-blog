from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.views.generic import ListView

from .models import Post, Comment
from .forms import CommentForm


#return home bage for users
def home_page(request):

    return render(request, 'blog/home.html')

# get 3 posts in list.html
def posts_list(request):

    post_list = Post.objects.all()
    paginator = Paginator(post_list, 3)

    try:
        posts = paginator.page(request.GET.get("page", 1))
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts':posts})

# you can use this way
# class PostsListViwe(ListView):

#     model = Post
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = "blog/post/list.html"

#get one post py id
def post_detail(request, post):

    try:
        post = Post.objects.get(slug=post)
        comments = Comment.objects.filter(post=post)

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
        else:
            form = CommentForm()

    except Post.DoesNotExist:
        return render (request, 'blog/post/post404.html')

    return render(request, 'blog/post/detail.html', {'post':post, 'form':form, 'comments':comments})
