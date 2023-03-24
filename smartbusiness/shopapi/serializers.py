from rest_framework import serializers
from .models import user_details,product,user_cart,orders_details,orders_transactions,complaints

class userSerializer(serializers.ModelSerializer):
	class Meta:
		model = user_details
		fields ='__all__'

class productSerializer(serializers.ModelSerializer):
	class Meta:
		model = product
		fields ='__all__'

class cartSerializer(serializers.ModelSerializer):
	class Meta:
		model = user_cart
		fields ='__all__'  

class orderSerializer(serializers.ModelSerializer):
	class Meta:
		model = orders_details
		fields ='__all__'  

class transactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = orders_transactions
		fields ='__all__'  

class complaintSerializer(serializers.ModelSerializer):
	class Meta:
		model = complaints
		fields ='__all__'