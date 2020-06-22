from django.test import TestCase, Client
from django.db.models import QuerySet
from django.urls import reverse
from image_uploads.models import Photo
from image_uploads.forms import ImageUploadForm
from image_uploads.utils import get_image_hash


class ImageListViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
        super().setUp()

    def test_get(self):
        Photo.objects.all().delete()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.context['photos'], QuerySet)


class ImageDetailViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.file = open('image_uploads/tests/files/pepug.jpg', 'rb')
        self.photo = Photo(name='1.jpg')
        self.photo.image.save('1.jpg', self.file)
        self.photo.save()
        self.url = reverse('image-detail', args=(self.photo.name,))
        super().setUp()

    def test_get(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['content-type'], 'image/jpeg')
        self.assertEqual(resp.content, self.photo.image.read())

    def test_get_404(self):
        url = reverse('image-detail', args=('non-exists.jpg',))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get(url, data=dict(width=512, height=''))
        self.assertEqual(resp.status_code, 404)

    def test_get_resize_image(self):
        params = dict(width=512, height=512, size=32000)
        resp = self.client.get(self.url, data=params)
        self.assertEqual(resp.status_code, 200)
        thumb = self.photo.thumbnails.get(**params)
        self.assertEqual(resp.content, thumb.image.read())


class ImageUploadViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('upload')
        self.file = open('image_uploads/tests/files/pepug.jpg', 'rb')
        super().setUp()

    def test_get(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.context['form'], ImageUploadForm)

    def test_post(self):
        resp = self.client.post(self.url, data={'url': '', 'file': self.file})
        self.file.seek(0)
        self.assertEqual(resp.status_code, 302)
        photo = Photo.objects.first()
        self.assertRedirects(resp, photo.get_absolute_url())