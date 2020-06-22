from django.urls import path
from .views import ImageListView, ImageUploadView, ImageDetailView

urlpatterns = [
    path('', ImageListView.as_view(), name='index'),
    path('upload/', ImageUploadView.as_view(), name='upload'),
    path('<str:image_name>/', ImageDetailView.as_view(), name='image-detail'),

]