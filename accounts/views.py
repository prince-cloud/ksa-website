from django.contrib import messages
from .forms import NewPasswordForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from vote_app.sms import Sms, SmsApi
from django.contrib.auth import get_user_model
from .utils import generate_password
# Create your views here.

User = get_user_model()

import secrets

""" def generate_password(request: HttpRequest) -> HttpResponse:
    password = secrets.token_urlsafe(10)
    return JsonResponse({'success': True, 'password': password})
 """


def get_new_password(request):
    if request.method == "POST":
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone_number: str = cd['phone_number']
            phone_number = phone_number.strip()
            try:
                member = get_object_or_404(User, username=phone_number)
            except:
                messages.error(request, "Sorry, you number does not exist, please contact your EC")
                return redirect('/accounts/new-password/')
            new_password = generate_password(7)
            member.set_password(new_password)
            member.save()
            sms = Sms()

            messages.success(request, "Password reset successful. An sms has been sent to your phone containing the new password")
            sms.send_message(recipients=[member.phone_number],message= f"Password Reset Successful. Login at https://https://knuststudentactivists.org/elections/ with        password: {new_password}", sender='KSA-EC')
            return redirect("/elections/")
    else:
        form = NewPasswordForm()
    return render(request, "accounts/generate_new_password.html", {'form': form})