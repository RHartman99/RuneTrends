from django.shortcuts import render
from .models import Item
from .constants import URLS
from datetime import datetime


def index(request):
    items = Item.objects.order_by("?")[:20]
    context = {"items": items, "cloudinary": URLS["CLOUDINARY"]}
    return render(request, "index.html", context)


def item(request, name):
    name = name.replace("_", " ")
    item = Item.objects.filter(name__iexact=name).first()
    context = {"item": item, "cloudinary": URLS["CLOUDINARY"]}
    if item.release_date is not None:
        context["release_date"] = item.release_date.strftime("%b %e, %Y")
    return render(request, "item.html", context)

