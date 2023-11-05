from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from main.models import Item


# Create your views here.

def homepage(request):
    return render(request=request, template_name='main/home.html')


def itemspage(request):
    if request.method == 'GET':
        items = Item.objects.filter(owner__item=None)
        context = {
            'items': items
        }
        return render(request=request, template_name='main/items.html', context=context)
    if request.method == 'POST':
        purchased_item = request.POST.get('purchased-item')
        if purchased_item:
            purchased_item_object = Item.objects.get(name=purchased_item)
            purchased_item_object.owner = request.user
            purchased_item_object.save()
            messages.success(request=request,
                             message=f'Congratulations! You just bought {purchased_item_object} for {purchased_item_object.price}')
        return redirect('items')


def loginpage(request):
    if request.method == 'GET':
        return render(request=request, template_name='main/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect('items')
        else:
            return redirect('login')


def logoutpage(request):
    logout(request=request)
    messages.success(
        request=request,
        message=f'You have been logged out')
    return redirect('home')


def registerpage(request):
    if request.method == 'GET':
        return render(request=request, template_name='main/register.html')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request=request, user=user)
            messages.success(
                request=request,
                message=f'You have registered your account successfully! Logged in as {username}')
            return redirect('home')
        else:
            messages.error(request=request, message=f'Account registration was unsuccessfull with errors: {form.errors}')
            return redirect('register')
