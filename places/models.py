from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from PIL import Image as Image


class Place(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    city = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    price = models.FloatField(default=0)
    thumbnail = models.ImageField(upload_to='place_pics/tn/', default='default.jpg')

    @property
    def images_list(self):
        return [i.image.url for i in self.images.all()]

    @property
    def score(self):
        scores = [review.score for review in self.reviews.all()]
        if len(scores) != 0:
            score = sum(scores) / len(scores)
            return round(score, 1)
        return 0.0

    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.thumbnail.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)



class PlaceImage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='place_pics', default='default.jpg', blank=True, null=True)




class Reservation(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reservations')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField(default=timezone.now)
    start_hour = models.TimeField(default=timezone.now)
    end_hour = models.TimeField(default=timezone.now)


class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    comment = models.TextField(max_length=500)
    score = models.DecimalField(max_digits=3, decimal_places=1,
                                validators=[MaxValueValidator(10), MinValueValidator(0)], default=0.0)
