from django.test import TestCase
from image_uploads.models import Photo, PhotoCache

from pathlib import Path


class PhotoTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = Path('image_uploads/tests/files/pepug.jpg')
        cls.photo = Photo()
        cls.photo.image.save(cls.path.name, open(cls.path, 'rb'))
        cls.photo.save()
        super().setUpClass()

    def test_create(self):
        photo_path = Path(self.photo.image.path)
        self.assertTrue(photo_path.exists())

    def test_make_thumbnail_without_parameters(self):
        with self.assertRaises(ValueError):
            thumb = self.photo.make_thumbnail()

    def test_make_thumbnail_impossible_size(self):
        with self.assertRaises(ValueError):
            thumb = self.photo.make_thumbnail(size=1)

    def test_make_thumbnail_hit_cache(self):
        params = dict(width=512, height=512, size=26000)
        cache1 = PhotoCache(**params, photo=self.photo)
        cache1.save()
        cache2 = self.photo.make_thumbnail(**params)
        self.assertEqual(cache1, cache2)
        self.assertEqual(PhotoCache.objects.count(), 1)

    def test_make_thumbnail(self):
        params = dict(width=512, height=512, size=10000)
        thumb = self.photo.make_thumbnail(**params)
        self.assertLessEqual(thumb.image.width, params['width'])
        self.assertLessEqual(thumb.image.height, params['height'])
        self.assertLessEqual(thumb.image.size, params['size'])

    @classmethod
    def tearDownClass(cls):
        Photo.objects.all().delete()
        super().tearDownClass()
