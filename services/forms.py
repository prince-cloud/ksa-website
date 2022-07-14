from dataclasses import field
from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget

class DateInput(forms.DateInput):
    input_type = "date"


class BecomAMemberForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=DateInput,
        label="Expiry Date",
    )
    class Meta:
        model = Member
        fields = (
            "full_name",
            "date_of_birth",
            "email_address",
            "programe_of_study",
            "phone_number",
            "membership_status",
            "place_of_residence",
            "name_of_current_hostel",

        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 w-100 mw-100'
                    'text-gray-700 border border-gray-200 '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                    'rounded py-1 px-2 leading-tight '
                )
            })

class HelpDeskForm(forms.ModelForm):
    class Meta:
        model = Helpdesk
        fields = (
            "issue",
            "content",
            "email_or_phone",
        )
        widgets = {
            "content": forms.Textarea(attrs={"rows": 6, "cols": 15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 w-100 mw-100'
                    'text-gray-700 border border-gray-200 '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                    'rounded py-1 px-2 leading-tight '
                )
            })


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "title_image",
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 w-100 mw-100'
                    'text-gray-700 border border-gray-200 '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                    'rounded py-1 px-2 leading-tight '
                )
            })