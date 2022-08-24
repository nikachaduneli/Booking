from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth.views import LoginView
from places.helpers import paginate
from places.models import Place


@unauthenticated_user
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request,'users/register.html', context=context)


class UserLoginView(LoginView):
    template_name = 'users/login.html'

    @unauthenticated_user
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    @unauthenticated_user
    def post(self, request, *args, **kwargs):
        return super().post(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

@login_required(login_url='login')
def my_places(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid:
            u_form.save()
            messages.success(request, 'Your Information Has Been Updated.')
            return redirect('my_places')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'title': f'{request.user.username}\'s Profile',
        'search': True,
    }
    places = Place.objects.filter(owner_id=request.user.id).order_by('-date_posted')
    paginator = paginate(paginate_by=10, objects=places, request=request)
    context.update(paginator)

    return render(request, 'users/profile.html', context=context)
