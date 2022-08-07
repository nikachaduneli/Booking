from .models import Place, Image, Reservation
from .forms import ImageForm, PlaceForm, ReviewForm, ReservationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .filters import PlaceFilter
from .helpers import paginate, reservation_already_exists
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.db.models.query import QuerySet
from django.db.models import Count
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from .decorators import allwed_users


class PlaceListView(ListView):
    model = Place
    template_name = 'places/place_list.html'

    paginate_by = 10

    def get(self, request, *args, **kwargs):
        places = Place.objects.all().order_by('-date_posted')
        place_filter = PlaceFilter(request.GET, queryset=places)
        places = place_filter.qs
        paginator = paginate(self.paginate_by, places, request)
        context = {'filter': place_filter, 'title': 'home'}
        context.update(paginator)
        return render(request, 'places/place_list.html', context)


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'places/place_detail.html'

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(request.POST)
        reservation_form = ReservationForm(request.POST)

        place = self.get_object()


        if review_form.is_valid():
            review_form.instance.author = request.user
            review_form.instance.place = place
            review_form.save()

        if reservation_form.is_valid():

            if reservation_already_exists(reservation_form.cleaned_data, place.id):
                messages.error(request, 'reservation on that time already exists')
                return redirect('place_detail', pk=place.id)

            reservation_form.instance.author = request.user
            reservation_form.instance.place = place
            reservation_form.save()

        return redirect('place_detail', pk=place.id)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['review_form'] = ReviewForm
        context['res_form'] = ReservationForm
        return context


class PlaceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Place
    fields = ['name', 'city', 'address', 'price', 'description']
    template_name = 'places/create_new_place.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        for image in request.FILES.getlist('image'):
            Image.objects.create(place=self.object, image=image)

        return super().post(request, *args, **kwargs)

    # def get_success_url(self):

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        place = self.get_object()
        if self.request.user == place.owner:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.object.name}'
        context['update'] = True
        context['image_form'] = ImageForm()
        return context


class PlaceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Place
    template_name = 'places/place_delete.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.object.name}'
        return context

    def test_func(self):
        place = self.get_object()
        if self.request.user == place.owner:
            return True
        return False


@allwed_users(allowed_roles='owner')
@login_required(login_url='login')
def create_place(request, *args, **kwargs):
    if request.method == "POST":
        place_form = PlaceForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES, prefix='image')
        if place_form.is_valid():
            place = place_form.save(commit=False)
            place.owner = request.user
            place.save()
            images = request.FILES.getlist('image')
            for image in images:
                Image.objects.create(place=place, image=image)

            messages.success(request, "New place Added")
            return redirect("place_list")
        else:
            messages.error(request, f'{place_form.errors}')
    else:
        place_form = PlaceForm()
        image_form = ImageForm()

    context = {'form': place_form,
               'image_form': image_form,
               'title': 'Create'}

    return render(request, "places/create_new_place.html", context)