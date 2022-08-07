from django import forms
from .models import PlaceImage, Place, Review, Reservation
from django.core.validators import MinValueValidator, MaxValueValidator


class PlaceForm(forms.ModelForm):
    price = forms.CharField()

    class Meta:
        model = Place
        fields = ['name', 'city', 'address', 'description', 'price']


class PlaceImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

    image = forms.ImageField(label='images',
                             widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = PlaceImage
        fields = ['image']


class ReviewForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '4',
        'class': 'md-textarea form-control'

    }))

    score = forms.ChoiceField(choices=((None, '-----'),
                                       (1, '1'),
                                       (2, '2'),
                                       (3, '3'),
                                       (4, '4'),
                                       (5, '5'),
                                       (6, '6'),
                                       (7, '7'),
                                       (8, '8'),
                                       (9, '9'),
                                       (10, '10')))

    class Meta:
        model = Review
        fields = ['comment', 'score']


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.DateInput):
    input_type = 'time'


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'start_hour', 'end_hour']
        widgets = {
            'date': DateInput(),
            'start_hour': TimeInput(),
            'end_hour': TimeInput()
        }
