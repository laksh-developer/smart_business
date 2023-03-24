from django.contrib import admin
from .models import user_details,product,user_cart,orders_details,orders_transactions,complaints
# Register your models here.
admin.site.register(user_details)
admin.site.register(product)
admin.site.register(user_cart)
admin.site.register(orders_details)
admin.site.register(orders_transactions)
admin.site.register(complaints)