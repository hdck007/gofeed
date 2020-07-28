from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views.generic import View

def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.is_active = False
      user.save()
      username = form.cleaned_data.get('username')
      current_site = get_current_site(request)
      email_subject = 'Activate Your Account'
      message = render_to_string('users/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
      to_email = form.cleaned_data.get('email')
      email = EmailMessage(email_subject, message, to=[to_email])
      email.send()
      return HttpResponse('<h1 style="text-align: center;">Check your email inbox for activation link!</h1>')
    else:
      messages.error(request, f'Please recheck your form and details below!')
  else:
    form = UserRegistrationForm()
  return render(request, 'users/register.html', {'form':form})
  
@login_required  
def profile(request):
  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST,
                              request.FILES,
                              instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, f'Your account has been updated succesfully!')
      return redirect('profile')
      
  else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm()
    
  context = {
    'u_form': u_form,
    'p_form': p_form
  }
  
  return render(request, 'users/profile.html', context)
  
class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
      try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
      except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
      if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, ('Your account have been confirmed. Start reading posts by clicking on the titles of the Blog-Posts'))
        return redirect('blog-home')
      else:
        return HttpResponse('<h2>The activation link is invalid</h2>')
