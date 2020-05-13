from django.shortcuts import render, redirect
from django.template.loader import render_to_string, get_template
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.views import generic
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import login
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            curr_site = get_current_site(request)
            subject='Activate Your Doubts Account'
            message = render_to_string('account_activation_email.html',{
                'user':user,
                'domain':curr_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('email_verification_done')
    else:
        form=UserRegisterForm()
    return render(request, 'users/signup.html', {'form':form})

def email_verification_confirm(request, uidb64, token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user= User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.profile.verified_email = True
        user.save()
        login(request, user)
        return redirect('doubts:index')
    else:
        return render(request, 'account_activation_invalid.html')
def email_verification_done(request):
    return render(request, 'email_veri_done.html')
