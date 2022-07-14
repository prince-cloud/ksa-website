from importlib.metadata import files
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from . forms import *
#from django.contrib.  import login
# Create your views here.
def secrete_route(request):
    helps = Helpdesk.objects.all()
    members = Member.objects.all()
    gallery = Gallery.objects.all()
    posts = Post.objects.all()
    yeargroup = YearGroup.objects.all()
    return render(request, 'pages/admin/admin_page.html',
    {
        "helps": helps,
        "members": members,
        "gallery": gallery,
        "posts": posts,
        "yeargroup": yeargroup,
    })

def executives(request):
    yeargroups = YearGroup.objects.all()
    return render(request, 'pages/admin/executives.html',
    {
        "yeargroups": yeargroups,
    })

def members(request):
    members = Member.objects.all()
    return render(request, 'pages/admin/members.html', {
        "members": members,
    })
    
def ksaHelpDesk(request):
    helps = Helpdesk.objects.all()
    return render(request, 'pages/admin/helpdesk.html', {
        "helps": helps,
    })
    
def posts(request):
    posts = Post.objects.all()
    return render(request, 'pages/admin/posts.html', {
        "posts": posts,
    })

def add_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            #data = form.cleaned_data()
            post_form = form.save(commit=False)
            post_form.posted_by = request.user
            post_form.save()
            return redirect("/posts/")
        else:
            print("Invalid data entry")
    else:
        form = PostForm()

    return render(request, 'pages/admin/add_post.html', {
        "form": form,
    })

    
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


def help_desk(request):
    if request.method == 'POST':
        help_desk_form = HelpDeskForm(data=request.POST, files=request.FILES)
        if help_desk_form.is_valid():
            help_desk_form.save()
            return redirect("/")
    else:
        help_desk_form = HelpDeskForm()
    
    return render(request, 'pages/help-desk.html', {
        "help_desk_form":help_desk_form
    })

def gallery(request):
    images = Gallery.objects.all()
    return render(request, 'pages/gallery.html', {
        "images": images
    })

def contact_us(request):
    return render(request, 'pages/contact_us.html')