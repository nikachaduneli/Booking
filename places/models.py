from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import sys
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image as pil_image
sys.path.append("..")
from users.models import User


class Place(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_posted = models.DateField(default=timezone.now)
    city = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    price = models.FloatField(default=0)

    @property
    def images_list(self):
        return [i.image.url for i in self.images.all()]

    @property
    def score(self):
        scores = [review.score for review in self.reviews.all()]
        if len(scores) != 0:
            score =  sum(scores) / len(scores)
            return round(score, 1)
        return 0.0

    def get_absolute_url(self):
        return reverse('place_list')

    def __str__(self):
        return self.name


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='place_pics', default='default.jpg', blank=True, null=True)


class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    comment = models.TextField(max_length=500)
    score = models.DecimalField(max_digits=3, decimal_places=1, validators=[MaxValueValidator(10),MinValueValidator(0)],default=0.0)
