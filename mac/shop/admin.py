from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Contact
from .models import Order
from .models import OrderUpdate

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)
