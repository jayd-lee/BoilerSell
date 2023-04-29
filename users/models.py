from django.core.files.storage import default_storage as storage
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    description = models.TextField(max_length=125, default='', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image_read = storage.open(self.image.name, "rb")
        img = Image.open(image_read)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)

            fh = storage.open(self.image.name, "wb")
            format = 'png'  # You need to set the correct image format here
            img.save(fh, format)
            fh.close()
    

