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
                messages.error(request, 'something went wrong try again')
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
