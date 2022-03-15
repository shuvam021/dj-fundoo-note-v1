from django.db import models


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)


class Label(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    note = models.ManyToManyField('notes.Note')
    color = models.CharField(max_length=50)
