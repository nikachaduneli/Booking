from django import forms
from .models import PlaceImage, Place, Review, Reservation
from django.core.exceptions import ValidationError


class PlaceForm(forms.ModelForm):
    price = forms.CharField()

    class Meta:
        model = Place
        fields = ['name', 'city', 'address', 'description', 'price']


class PlaceImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))

    def clean(self):
        cleaned_date = super(PlaceImageForm, self).clean()
        image_extensions = ['jpeg', 'png', 'jpg', 'gif', 'psd', 'pdf', 'eps', 'webp']
        images = self.files.getlist('image')
        if len(images) > 0:
            for image in images:
                ext = image.name.split('.')[-1]
                if ext.lower() not in image_extensions:
                    raise ValidationError({'image': 'invalid image type "%s"' % ext})
        return cleaned_date

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
