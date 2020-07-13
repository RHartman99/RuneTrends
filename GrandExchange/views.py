from django.shortcuts import render
from .models import Item


def index(request):
    items = Item.objects.order_by("name")[:20]
    context = {"items": items}
    return render(request, "index.html", context)
