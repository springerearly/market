from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from main.models import Item


# Create your views here.

def homepage(request):
    return render(request=request, template_name='main/home.html')


def itemspage(request):
    if request.method == 'GET':
        items = Item.objects.exclude(owner__username=request.user.username).filter(is_for_sale=True)
        context = {
            'items': items,
            'items_page': True,

        }
        return render(request=request, template_name='main/items.html', context=context)
    if request.method == 'POST':
        purchased_item_id = request.POST.get('purchased-item-id')
        if purchased_item_id:
            purchased_item_object = Item.objects.get(pk=purchased_item_id)
            purchased_item_object.owner = request.user
            purchased_item_object.is_for_sale = False
            purchased_item_object.save()
            messages.success(request=request,
                             message=f'Congratulations! You just bought \
                             {purchased_item_object} for \
                             {purchased_item_object.price}')
        return redirect('items')


def my_itemspage(request):
    if request.method == 'GET':
        items = Item.objects.filter(owner__username=request.user.username)
        context = {
            'items': items,
            'items_page': False,
        }
        return render(request=request, template_name='main/items.html', context=context)
    if request.method == 'POST':
        item_for_sale_id = request.POST.get('item-for-sale-id')
        new_price = request.POST.get('new-price')
        new_description = request.POST.get('new-description')
        if item_for_sale_id and new_price and new_description:
            item_for_sale_object = Item.objects.get(pk=item_for_sale_id)
            item_for_sale_object.price = new_price
            item_for_sale_object.description = new_description
            item_for_sale_object.is_for_sale = True
            item_for_sale_object.save()
            messages.success(request=request,
                             message=f'Congratulations! \
                             You just bought {item_for_sale_object.name} \
                             for {item_for_sale_object.price}')
        return redirect('my-items')


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

        return redirect('login')


def logoutpage(request):
    logout(request=request)
    messages.success(
        request=request,
        message='You have been logged out')
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

        messages.error(request=request,
                           message=form.errors)
        return redirect('register')
