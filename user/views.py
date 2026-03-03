from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.models import User
from .forms import CreateRegisterForm, UpdateProfileForm


# Class based functions
class LoginView(BaseLoginView):
    template_name = 'user/auth/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.headers.get('HX-Request'):
            redirect_url = resolve_url(self.get_success_url())
            hx_response = HttpResponse()
            hx_response['HX-Redirect'] = redirect_url
            return hx_response
        
        return response

def index(request):
    return render(request, 'user/auth/page.html') 

def register(request):
    if request.method == 'POST':
        form = CreateRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            if request.headers.get("HX-Request"):
                response = HttpResponse()
                response['HX-Redirect'] = redirect('dashboard-home').url
                return response

            return redirect('dashboard-home')
    else:
        form = CreateRegisterForm()

    context = {
        'form': form
    }

    return render(request, 'user/auth/register.html', context)

def reset(request):
    return render(request, 'user/auth/password_reset.html')

def profile(request):
    user = request.user
    context = {
        'fullname': f'{user.first_name} {user.last_name}',
        'position': user.profile.position,
        'department': user.profile.get_department_display(),
        'email': user.email,
        'phone_number': user.profile.phone_number
    }
    return render(request, 'user/profile.html', context)
 
def profile_update(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else: 
        form = UpdateProfileForm(instance=request.user)

    context = {
        'form': form
    }

    return render(request, 'user/profile_update_form.html', context)
