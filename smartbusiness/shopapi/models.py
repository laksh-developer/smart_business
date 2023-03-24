from django.db import models

# Create your models here.

# Create your models here.
class user_details(models.Model):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    mobile = models.BigIntegerField(unique=True)
    shop_name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    place = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    user_type=models.CharField(choices=[('Retailer','Retailer'),('Distributor','Distributor')],max_length=50)
    is_approved = models.BooleanField(default=False) 

    def __str__(self):
        return (self.username+" -> status: "+str(self.is_approved))
    
class product(models.Model):
    distributor = models.ForeignKey(user_details, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    price = models.BigIntegerField()
    quantity = models.IntegerField()
    qty_metrics=models.CharField(default=None,max_length=100,blank=True)
    image = models.ImageField(upload_to='pics',null=True,default="",blank=True)
    manufacturer = models.CharField(max_length=100)
    product_category=models.CharField(max_length=100,default=None,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (str(self.id))
    
class user_cart(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product,on_delete=models.CASCADE)
    price = models.BigIntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return (str(self.id))
    

class orders_details(models.Model):
    razorpay_order_id=models.CharField(default=None,max_length=100,blank=True)
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    product_id = models.ForeignKey(product, on_delete=models.CASCADE)
    distributor = models.IntegerField()
    price = models.BigIntegerField()
    quantity = models.IntegerField()
    delivery_status=models.CharField(choices=[('Order Confirmed','Order Confirmed'),('Delivery In Process','Delivery In Process'),('Order Delivered','Order Delivered')],max_length=50)
    amount_paid = models.BooleanField(default=False)
    payment_mode=models.CharField(choices=[('Online','Online'),('Offline','Offline')],max_length=50)
    is_delivered = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return (self.user.username)
    
class orders_transactions(models.Model):
    razorpay_order_id=models.CharField(default=None,max_length=200,blank=True)
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    distributor = models.IntegerField()
    price = models.BigIntegerField()
    payment_id=models.CharField(default=None,max_length=200,blank=True)
    status=models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return (self.user.username)


class complaints(models.Model):
    distributor = models.ForeignKey(user_details, on_delete=models.CASCADE,related_name='distributor')
    user=models.ForeignKey(user_details, on_delete=models.CASCADE,related_name='retailer')
    its_id = models.CharField(max_length=200)
    complaint_on=models.CharField(choices=[('Product','Product'),('Orders','Orders'),('Payment','Payment')],max_length=50)
    complaint_book_date = models.DateTimeField(auto_now_add=True)
    complaint_details=models.CharField(max_length=200)
    is_complaint_closed=models.BooleanField(default=False)
    reply=models.CharField(max_length=200,blank=True,null=True,default=None)
    complaint_complete_date = models.DateTimeField(auto_now=True)

