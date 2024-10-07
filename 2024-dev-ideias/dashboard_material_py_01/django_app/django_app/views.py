# django_app/views.py

from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import ImageUpload


from django.core.paginator import Paginator


def home(request):
    image_list = ImageUpload.objects.all()
    paginator = Paginator(image_list, 5)  # 5 imagens por página
    page_number = request.GET.get("page")
    images = paginator.get_page(page_number)
    return render(request, "index.html", {"images": images})


def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("display_images")
    else:
        form = ImageUploadForm()
    return render(request, "upload.html", {"form": form})


def display_images(request):
    images = ImageUpload.objects.all()
    return render(request, "index.html", {"images": images})
