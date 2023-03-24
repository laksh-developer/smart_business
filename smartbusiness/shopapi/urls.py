
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_user),
    path('login', views.login),
    path('get_user/<str:uname>', views.get_user),
    path('searchproduct/<str:pname>', views.search_product),
    path('dsearchproduct/<str:pname>', views.distributor_search_product),
    path('saveproduct', views.save_product),
    path('allproducts', views.get_all_products),
    path('getproduct/<int:id>', views.get_product),
    path('dproduct/<int:id>', views.get_product_distributor),
    path('get_user_by_id/<int:id>', views.get_user_by_id),
    path('addtocart', views.add_to_cart),
    path('orders', views.orders),
    path('paymenthandler', views.paymenthandler, name='paymenthandler'),
    path('userorders/<int:id>', views.get_user_orders),
    path('usertransact/<int:id>', views.get_user_transact),
    path('disorders/<int:id>', views.get_dis_orders),
    path('updateproductdata/<int:id>', views.up_product_data),
    path('updateproduct', views.up_product),
    path('delete_product/<int:id>', views.del_product),
    path('deliver_order/<str:id>', views.deliver_order),
    path('searchtransact/<str:s>', views.search_transact),
    path('offlinepay', views.offlinepay),
    path('makecomplaint', views.makecomplaint),
    path('replycomplaint/<int:id>', views.replycomplaint),
    path('finishcomplaint/<int:id>', views.finishcomplaint),
    path('dcomplaint/<int:id>', views.getcomplaintd),
    path('rcomplaint/<int:id>', views.getcomplaintr),
    path('cartdata/<int:id>', views.getcartdata),
    path('deletefromcart/<int:id>', views.deletefromcart),

]
