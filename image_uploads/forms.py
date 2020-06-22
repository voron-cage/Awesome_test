from django import forms
from image_uploads.utils import download_image
from image_uploads.models import Photo
from uuid import uuid4


class ImageUploadForm(forms.Form):
    url = forms.CharField(max_length=2048, required=False)
    file = forms.FileField(required=False)

    def clean(self):
        data = self.cleaned_data
        if not data['url'] and data['file'] is None:
            raise forms.ValidationError("Одно из полей необходимо заполнить")

    def save(self, image):
        """
        Сохраняем файл в бд если нет совпадений по хэшу
        """
        image_name = f'{uuid4().hex}.jpg'
        photo = Photo(name=image_name)
        photo.image.save(image_name, image)
        photo.save()
        return photo

    def save_from_url(self):
        """
        Скачиваем изображение по url адресу
        """
        url = self.cleaned_data.get('url')
        image = download_image(url)
        if image:
            return self.save(image)

    def save_from_file(self):
        file = self.cleaned_data.get('file')
        return self.save(file)
