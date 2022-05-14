from distutils.command.upload import upload
from importlib.metadata import requires
from pyexpat import model
from random import choices
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import SlugField
from django.utils.text import slugify

User = get_user_model()
# Create your models here.

MEMBERSHIP_STATUS = (
    ("Undergraduate", "Undergraduate"),
    ("Graduate/NSP", "Graduate/NSP"),
    ("Postgraduate/Schooling","Postgraduate/Schooling"),
    ("Alumni", "Alumni")
)

ISSUES = (
    ("Welfare", "Welfare"),
    ("Academic", "Academic"),
    ("Isses with Hall/Hostel", "Isses with Hall/Hostel"),
    ("Report Abuse", "Report Abuse"),
    ("Other", "Other")
)

class Member(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(help_text="this helps us to wish you a happy birthday when its your birthday")
    email_address = models.EmailField()
    programe_of_study = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    membership_status = models.CharField(choices=MEMBERSHIP_STATUS, max_length=50)
    place_of_residence = models.CharField(max_length=100)
    name_of_current_hostel = models.CharField(max_length=100)


    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class PostImage(models.Model):
    image = models.ImageField(upload_to="posts_multiple_image/")
    

class Post(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    title_image = models.ImageField(upload_to="posts_images/")
    content = models.CharField(max_length=200)

    multiple_images = models.ForeignKey(PostImage, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    slug = models.SlugField(blank=True, null=True)


    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)


class Helpdesk(models.Model):
    issue = models.CharField(choices=ISSUES, max_length=50)
    content = models.TextField()
    email_or_phone = models.CharField(max_length=50, blank=True, null=True)
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.issue
    

class Gallery(models.Model):
    image = models.ImageField(upload_to='Gallery')

    def __str__(self) -> str:
        return self.image