from distutils.command.upload import upload
from importlib.metadata import requires
from pyexpat import model
from random import choices
from turtle import position
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import SlugField
from django.utils.text import slugify
from ckeditor.fields import RichTextField

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

class Position (models.Model):
    position = models.CharField(max_length=100)

    class Meta:
        ordering = ("position", )
    def __str__(self) -> str:
        return self.position

class YearGroup(models.Model):
    year = models.CharField(max_length=50)

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)
    def __str__(self) -> str:
        return self.year

class Executive(models.Model):
    year = models.ForeignKey(YearGroup, max_length=100, on_delete=models.SET_NULL, null=True, related_name="executives")
    name = models.CharField(max_length=200)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    profile_pic = models.ImageField(upload_to="profile/")
    phone_number = models.CharField(max_length=14)

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


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
    content = RichTextField()

    multiple_images = models.ForeignKey(PostImage, on_delete=models.SET_NULL, null=True, blank=True, related_name="images")
    slug = models.SlugField(blank=True, null=True)


    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_posted",)

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
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date",)
        
    def __str__(self) -> str:
        return self.title


class Gallery(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name="images", blank=True)
    image = models.ImageField(upload_to='Gallery')

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return self.image

