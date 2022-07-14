from email import message
from importlib.metadata import files
from xmlrpc.client import DateTime
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from . forms import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

#from django.contrib.  import login
# Create your views here.
@staff_member_required
def secrete_route(request):
    helps = Helpdesk.objects.all()
    members = Member.objects.all()
    gallery = Gallery.objects.all()
    posts = Post.objects.all()
    yeargroup = YearGroup.objects.all()
    events = Event.objects.filter(date__gte = timezone.now())
    outdated_events = Event.objects.filter(date__lte = timezone.now())

    return render(request, 'pages/admin/admin_page.html',
    {
        "helps": helps,
        "members": members,
        "gallery": gallery,
        "posts": posts,
        "yeargroup": yeargroup,
        "events": events,
        "outdated_events": outdated_events,
    })

@staff_member_required
def executives(request):
    yeargroups = YearGroup.objects.all()
    return render(request, 'pages/admin/executives.html',
    {
        "yeargroups": yeargroups,
    })

@staff_member_required
def add_executive(request):
    if request.method == 'POST':
        form = ExecutiveForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/executives/')
        else:
            print("invalid data entry, please try again")
    else:
        form = ExecutiveForm()

    return render(request, 'pages/admin/add_executive.html', {
        "form": form,
    })

@staff_member_required
def add_yeargroup(request):
    if request.method == 'POST':
        form = YearGroupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/executives/')
        else:
            print("invalid data entry, please try again")
    else:
        form = YearGroupForm()

    return render(request, 'pages/admin/add_executive.html', {
        "form": form,
    })

@staff_member_required
def add_position(request):
    if request.method == 'POST':
        form = PositionForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Position added succesffuly")
            return redirect('/executives/')
        else:
            print("invalid data entry, please try again")
    else:
        form = PositionForm()

    return render(request, 'pages/admin/add_position.html', {
        "form": form,
    })

@staff_member_required
def members(request):
    members = Member.objects.all()
    return render(request, 'pages/admin/members.html', {
        "members": members,
    })

@staff_member_required    
def ksaHelpDesk(request):
    helps = Helpdesk.objects.all()
    return render(request, 'pages/admin/helpdesk.html', {
        "helps": helps,
    })

@staff_member_required  
def posts(request):
    posts = Post.objects.all()
    return render(request, 'pages/admin/posts.html', {
        "posts": posts,
    })

@staff_member_required
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

@staff_member_required
def postdetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render (request, "pages/post_detail.html",
    {
        "post":post,
    })
@staff_member_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    del_post = post
    del_post.delete()
    return redirect('/posts/')



@staff_member_required
def admin_gallery(request):
    images = Gallery.objects.all()
    return render(request, 'pages/admin/gallery.html', {
        "images": images
    })

@staff_member_required
def delete_gallery_image(request, id):
    image = get_object_or_404(Gallery, id=id)
    delete_image = image
    delete_image.delete()
    messages.success(request, 'Image succesfully deleted')
    return redirect("/admin-gallery/")


@staff_member_required
def upload_gallery_images(request):
    if request.method == "POST":
        form = GalleryForm(data=request.POST, files=request.FILES)
        images = request.FILES.getlist("image")
        if form.is_valid():
            data = form.cleaned_data
            gallery_form = form.save(commit=False)
            event = data['event']
            for image in images:
                Gallery.objects.create(
                    image = image,
                    event = event,
                )
            messages.success(request, 'Images succesfully added')
            gallery_form.save()
            return redirect("/admin-gallery/")
        else:
            messages.error(request, 'Images couldnt be uploaded. Please check and try again.')
    else:
        form = GalleryForm()
    return render(request, 'pages/admin/add_gallery_image.html', {
        "form": form,
    })

@staff_member_required
def events(request):
    events = Event.objects.filter(date__gte = timezone.now())
    outdated_events = Event.objects.filter(date__lte = timezone.now())

    return render(request, 'pages/admin/events.html', {
        "events": events,
        "outdated_events": outdated_events,

    })

@staff_member_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'event Successfully added')
            return redirect("/events/")
        else:
            print("Invalid data entry")
    else:
        form = EventForm()
    return render(request, 'pages/admin/add_event.html', {
        "form": form,
    })

@staff_member_required
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    del_event = event
    del_event.delete()
    messages.success(request, 'Event succesfully deleted')
    return redirect("/events/")
 
def index(request):
    posts = Post.objects.all()
    events = Event.objects.filter(date__gte = timezone.now())
    return render (request, 'pages/index.html', {
        "posts": posts,
        "events": events,

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
    events = Event.objects.all()
    return render(request, 'pages/gallery.html', {
        "images": images,
        "events": events
    })

def contact_us(request):
    return render(request, 'pages/contact_us.html')

def all_post(request):
    posts = Post.objects.all()
    return render (request, 'pages/all_posts.html', {
        "posts": posts,

    })