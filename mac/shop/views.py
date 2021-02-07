from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from .models import Contact
from math import ceil
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    allProds = []
    catProds = Product.objects.values('category')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category = cat)
        n = len(prod)
        nSlides = n // 4 + ceil(n/4 - n//4)
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {"allProds": allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

        con = Contact(name = name, email = email, phone = phone, desc = desc)
        con.save()
    return render(request, 'shop/contact.html')


def tracker(request):
    return render(request, 'shop/track.html')


def search(request):
    return HttpResponse("Search Anything you Like")


def productView(request, myid):
    product = Product.objects.filter(id = myid)
    print(product)
    return render(request, "shop/prodView.html", {'product': product[0]})


def checkout(request):
    return render(request, "shop/checkout.html")
