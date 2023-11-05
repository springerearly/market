from django.shortcuts import render, HttpResponse
from main.models import Item

# Create your views here.

def homepage(request):
    return render(request=request, template_name='main/home.html')


def itemspage(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request=request, template_name='main/items.html', context=context)
