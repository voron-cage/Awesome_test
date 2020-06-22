from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.generic import ListView, View, DetailView
from django.contrib import messages
from .models import Photo
from image_uploads.forms import ImageUploadForm


class ImageListView(ListView):
    template_name = 'image_uploads/image_list_view.html'
    queryset = Photo.objects.all()[:15]
    context_object_name = 'photos'


class ImageDetailView(DetailView):
    template_name = 'image_uploads/image_detail_view.html'

    def get(self, request, image_name):
        params = {
            'width': request.GET.get('width'),
            'height': request.GET.get('height'),
            'size': request.GET.get('size'),
            }
        for key in params:
            try:
                params[key] = int(params[key])
            except (TypeError, ValueError):
                params[key] = None
        photo = get_object_or_404(Photo, name=image_name)
        if params['width'] and params['height'] or params['size']:
            try:
                photo = photo.make_thumbnail(**params)
            except ValueError:
                return HttpResponse("Не удалось сформировать изображение по заданным параметрам", status=404)
        return HttpResponse(content=photo.image, content_type='image/jpeg')


class ImageUploadView(View):
    template_name = 'image_uploads/image_upload_view.html'
    form = ImageUploadForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['url']:
                photo = form.save_from_url()
            else:
                photo = form.save_from_file()
            if photo:
                return redirect(photo.get_absolute_url())
        return render(request, self.template_name, {'form': form})
