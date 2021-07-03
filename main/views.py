from django import template
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import AdvUser
from .forms import ChangeUserInfoForm,RegistrerUserForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from .utilities import signer

def user_activate(request,sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request,'bad_signature.html')
    user = get_object_or_404(AdvUser,username=username)
    if user.is_activated:
        template = 'user_is_activated.html'
    else:
        template = 'activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request,template)
    
class RegisterDoneView(TemplateView):
    template_name = 'main:register_done.html'

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'register_user.html'
    form_class = RegistrerUserForm
    success_url = reverse_lazy('main:register_done')

class BBPasswordChangeView(SuccessMessageMixin,LoginRequiredMixin,PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Parol ozgardi'


class ChangeUserInfoView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = AdvUser
    template_name = 'change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Foydalanuvchi malumoti ozgardi'

    def setup(self,request,*args,**kwargs):
        self.user_id = request.user.pk
        return super().setup(request,*args,**kwargs)
    def get_object(self,queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset,pk=self.user_id)
class BBLogoutView(LoginRequiredMixin,LogoutView):
    template_name = 'main/logout.html'
# Create your views here.
@login_required
def profile(request):
    return render(request,'main/profile.html')
class BBLoginView(LoginView):
    template_name = 'main/login.html'
def index(request):
    return render(request,'main/index.html')

def other_page(request,page):
    try:
        template = get_template('main/'+page+'.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))