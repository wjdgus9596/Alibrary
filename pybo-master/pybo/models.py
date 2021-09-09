from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    path = f'C:/Users/Administrator/PycharmProjects/pythonProject6/mysite/media/{instance.title}/{filename}.csv'
    return path

class User(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class UploadFileModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=user_directory_path)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Keyword(models.Model):
    number = models.TextField()
    unnamed = models.TextField()
    update = models.CharField(max_length=255)
    time = models.TextField()
    watch = models.TextField()
    search = models.TextField()
    leyword = models.TextField()
    video = models.TextField()
    url = models.URLField(blank=True, max_length=500)

    def __str__(self):
        return self.leyword