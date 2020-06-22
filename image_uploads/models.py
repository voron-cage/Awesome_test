from django.db import models
from PIL import Image
from uuid import uuid4
from django.urls import reverse

from io import BytesIO
import sys


class Thumbnail:

    def __init__(self, photo, width=None, height=None, size=None):
        self.photo = photo
        self.width = width
        self.height = height
        self.size = size
        self.resize = True
        self.limit_size = True

    def _validate(self):
        if any(val is None for val in [self.width, self.height]):
            self.resize = False
        if not self.size:
            self.limit_size = False
        if not self.resize and not self.limit_size:
            raise ValueError("Not enough parameters to create a thumbnail. Need to provide width and height or size")

    def get_cache_thumbnail(self):
        try:
            return self.photo.thumbnails.get(width=self.width, height=self.height, size=self.size)
        except PhotoCache.DoesNotExist:
            return

    def write_cache(self, file):
        image_name = f'{uuid4().hex}.jpg'
        cache = PhotoCache(photo=self.photo, width=self.width, height=self.height, size=self.size, name=image_name)
        cache.image.save(image_name, content=file)
        cache.save()
        return cache

    def _estimate_size(self, image):
        """
        Ухудшает кач-во изображения до тех пор пока размер не будет меньше или равен максимальному значению size.
        К сожалению, вывести зависимость между качеством изображения и её размером практически невозможно.
        Приходится итерационно уменьшать значение quality.
        https://stackoverflow.com/questions/4513648/how-to-estimate-the-size-of-jpeg-image-which-will-be-scaled-down
        """

        for i in reversed(range(0, 95+1)):
            img = self._save(image, quality=i)

            # Вычисляем размер изображения.
            img_size = sys.getsizeof(img) - sys.getsizeof(BytesIO())
            if img_size < self.size:
                return img

    def _save(self, image, quality=95):
        fp = BytesIO()
        image.save(fp, format='JPEG', quality=quality)
        fp.seek(0)
        return fp

    def make_thumbnail(self):
        self._validate()

        image = Image.open(self.photo.image)
        image = image.convert("RGB")
        if self.resize:
            image.thumbnail(size=(self.width, self.height), resample=Image.ANTIALIAS)
        if self.limit_size:
            return self._estimate_size(image)
        else:
            return self._save(image)


class Photo(models.Model):
    name = models.CharField(max_length=42)
    image = models.ImageField(upload_to='images/%y/%m/%d')

    def make_thumbnail(self, width=None, height=None, size=None):
        thumbnail = Thumbnail(photo=self, width=width, height=height, size=size)
        cache = thumbnail.get_cache_thumbnail()
        if cache:
            return cache
        file = thumbnail.make_thumbnail()
        if not file:
            raise ValueError("Failed to create image by specified parameters")
        return thumbnail.write_cache(file=file)

    def get_absolute_url(self):
        return reverse('image-detail', args=(self.name,))


class PhotoCache(models.Model):
    photo = models.ForeignKey(
        'image_uploads.Photo',
        on_delete=models.CASCADE,
        related_name='thumbnails',
    )
    name = models.CharField(max_length=42)
    image = models.ImageField(upload_to='cache/%y/%m/%d')
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    size = models.PositiveIntegerField(null=True)