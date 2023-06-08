from django.db import models

# Create your models here.

class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.text