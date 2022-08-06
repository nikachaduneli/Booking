from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import UserRegisterForm
from django.contrib import messages
from .decorators import unauthenticated_user
from django.contrib.auth.views import LoginView


@unauthenticated_user
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user_type = form.cleaned_data.get('user_type')
                if user_type == '1':
                    group = Group.objects.get(name='owner')
                elif user_type == '2':
                    group = Group.objects.get(name='costumer')
                else:
                    messages.error(request, 'invalid user type')
                    return redirect('register')

                # user.groups.add(group)
                return redirect('login')
            except:
                messages.error('something went wrong try again')
                return redirect('register')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'users/login.html'

    @unauthenticated_user
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    @unauthenticated_user
    def post(self, request, *args, **kwargs):
        return super().post(self, request, *args, **kwargs)