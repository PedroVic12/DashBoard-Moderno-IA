# django_app/models.py

from django.db import models


class ImageUpload(models.Model):
    image = models.ImageField(upload_to="imgs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded at {self.uploaded_at}"
