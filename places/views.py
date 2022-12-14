from .models import Place, PlaceImage, Reservation
from .forms import (
    PlaceImageForm,
    PlaceForm,
    ReviewForm,
    ReservationForm
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .filters import PlaceFilter
from .helpers import (
    paginate,
    reservation_already_exists
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from .decorators import allwed_users
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from datetime import date


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

    @method_decorator(login_required(login_url='login'))
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
                messages.error(request, 'Reservation On That Time Already Exists!')
                return redirect('place_detail', pk=place.id)
            if reservation_form.cleaned_data.get('date') < date.today():
                messages.error(request, 'Reservation Cant Be Created With Past Date!')
                return redirect('place_detail', pk=place.id)

            reservation_form.instance.author = request.user
            reservation_form.instance.place = place
            reservation_form.save()

        return redirect('place_detail', pk=place.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['review_form'] = ReviewForm
        context['res_form'] = ReservationForm
        return context


@api_view(['DELETE'])
def delete_reservation(request, *args, **kwargs):
    if request.method == 'DELETE':
        pk = kwargs.get('pk')
        reservation = Reservation.objects.filter(id=pk).first()
        if (reservation.date - date.today()).days < 1:
            raise ValidationError(detail={'detail': 'Reservation Date Is In Less than 1 Day And Cant Be Deleted!'})
        if reservation.author.id != request.user.id:
            raise PermissionDenied()
        reservation.delete()
        return Response({'message': 'reservation deleted'})


@api_view(['DELETE'])
def delete_image(request, *args, **kwargs):
    if request.method == 'DELETE':
        pk = kwargs.get('pk')
        image = PlaceImage.objects.filter(id=pk).first()
        if image.place.owner.id != request.user.id:
            raise PermissionDenied()
        image.delete()
        return Response({'message': 'reservation deleted'})


@allwed_users(allowed_roles=['Place Owner'])
@login_required(login_url='login')
def place_update(request, pk):
    place = get_object_or_404(Place, id=pk.get('pk'))
    if request.user.id != place.owner_id:
        return redirect('home')

    if request.method == "POST":
        place_form = PlaceForm(request.POST, instance=place)
        image_form = PlaceImageForm(request.POST, request.FILES)
        if place_form.is_valid() and image_form.is_valid():
            images = request.FILES.getlist('image')
            place_form.save()
            for image in images:
                PlaceImage.objects.create(place=place, image=image)
            messages.success(request, f'{place.name} Upadated')
            return redirect('place_detail', pk=place.id)
    else:
        place_form = PlaceForm(instance=place)
        image_form = PlaceImageForm()

    context = {'form': place_form,
               'image_form': image_form,
               'title': f'Update {place.name}',
               'object': place,
               'update': True
               }

    return render(request, 'places/create_new_place.html', context=context)


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


@allwed_users(allowed_roles=['Place Owner'])
@login_required(login_url='login')
def create_place(request, *args, **kwargs):
    if request.method == "POST":
        place_form = PlaceForm(request.POST)
        image_form = PlaceImageForm(request.POST, request.FILES)
        if place_form.is_valid() and image_form.is_valid():
            images = request.FILES.getlist('image')
            place = place_form.save(commit=False)
            place.owner = request.user
            place.save()
            if len(images) == 0:
                PlaceImage.objects.create(place=place)
            else:
                for image in images:
                    PlaceImage.objects.create(place=place, image=image)

            messages.success(request, "New place Added")
            return redirect("place_list")
    else:
        place_form = PlaceForm()
        image_form = PlaceImageForm()

    context = {'form': place_form,
               'image_form': image_form,
               'title': 'Create'}

    return render(request, "places/create_new_place.html", context)
