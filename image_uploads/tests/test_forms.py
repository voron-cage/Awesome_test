from django.test import TestCase
from image_uploads.models import Photo
from django.core.files.uploadedfile import SimpleUploadedFile
from image_uploads.forms import ImageUploadForm

from pathlib import Path


class ImageUploadFormTestCase(TestCase):

    def setUp(self):
        self.image_url = 'https://sun9-21.userapi.com/c855724/v855724564/249609/dWDRnoeVcvY.jpg'
        self.form = ImageUploadForm

    def test_without_data(self):
        form = self.form(data={})
        self.assertFalse(form.is_valid())
        self.assertIsNotNone(form.errors)

    def test_save_from_url(self):
        form = self.form(data={'url': self.image_url, 'path': None})
        self.assertTrue(form.is_valid())
        photo = form.save_from_url()
        self.assertIsNotNone(photo)
        self.assertTrue(Path(photo.image.path).exists())


