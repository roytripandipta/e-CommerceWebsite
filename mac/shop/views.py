from django.shortcuts import render
from django.http import HttpResponse
from django.utils.formats import date_format
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .models import Contact
from .models import Order
from .models import OrderUpdate
from math import ceil
import json
from PayTm import Checksum
from datetime import datetime
# import the logging library
import logging

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
    allProds = []
    catProds = Product.objects.values('category')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil(n / 4 - n // 4)
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

        con = Contact(name=name, email=email, phone=phone, desc=desc)
        con.save()
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == 'POST':
        order_id = request.POST.get('orderId', '')
        email = request.POST.get('email', '')

        try:
            order = Order.objects.filter(order_id = order_id, email = email)
            if len(order) > 0:
                updates = []
                update = OrderUpdate.objects.filter(order_id = order_id)
                for item in update:
                    formatted_datetime = date_format(item.timestamp)
                    print(formatted_datetime)
                    updates.append({'text' : item.update_desc, 'time': formatted_datetime})
                    response = json.dumps(updates, default = str)

                return HttpResponse(response)
            else:
                print("hello")
                return HttpResponse('{}')

        except Exception as e:
            print(e)
            return HttpResponse('{}')

    return render(request, 'shop/track.html')


def search(request):
    return HttpResponse("Search Anything you Like")


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, "shop/prodView.html", {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        itemsJson = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Order(items_json=itemsJson, name=name, email=email, address=address, city=city, state=state,
                      zip_code=zip_code, phone=phone, amount = amount)
        order.save()
        update = OrderUpdate(order_id = order.order_id, update_desc = "Your order has been placed")
        update.save()
        thank = True
        id = order.order_id
        #return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        param_dict = {
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': 'email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict["CHECKSUMHASH"] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')


# to bypass csrf
@csrf_exempt
def handlerequest(request):
    return HttpResponse("Done")