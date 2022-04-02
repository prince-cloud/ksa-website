from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from . forms import *
# Create your views here.

def index(request):
    posts = Post.objects.all()
    return render (request, 'pages/index.html', {
        "posts": posts,
    })

def postdetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render (request, "pages/post_detail.html",
    {
        "post":post,
    })

def become_a_member(request):
    if request.method == 'POST':
        membership_form = BecomAMemberForm(data=request.POST, files=request.FILES)
        if membership_form.is_valid():
            membership_form.save()
            return redirect("/")
    else:
        membership_form = BecomAMemberForm()
    return render(request, 'pages/become-a-memebr.html', {
        "membership_form": membership_form
    })