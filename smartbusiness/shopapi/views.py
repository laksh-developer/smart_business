from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import userSerializer,productSerializer,cartSerializer,orderSerializer,transactionSerializer,complaintSerializer		
from .models import user_details,product,user_cart,orders_details,orders_transactions,complaints
import razorpay

razorpay_client = razorpay.Client(auth=("rzp_test_kaMftty1cmOWWB", "CZDBzSJVrhPUJW9DcSiUWmP5"))

# Create your views here.
@api_view(['POST'])
def register_user(request):

    serializer = userSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user_obj=user_details.objects.get(username=request.POST.get('username'))
    else:
        return Response({'error':True,
        'errors':serializer.errors
        
        })
    return Response({
        'approval':user_obj.is_approved ,
        'error':False,
        'username':request.POST.get('username'),
        'password':request.POST.get('password')
    }) 

@api_view(['POST'])
def login(request):
    uname=request.POST.get('username')
    pwd=request.POST.get('password')
    try:
        userobj=user_details.objects.get(username=uname,password=pwd)
        return Response({
        'approval':userobj.is_approved,
        'error':False,
        'id':userobj.id,
        'user_type':userobj.user_type,
        'username':request.POST.get('username'),
        'password':request.POST.get('password')
    })
    except user_details.DoesNotExist:
        return Response({'error':True,
        'errors':'User Dont exist please register!'
        
        }) 

@api_view(['GET'])
def get_user(request,uname):
    
    try:
        user=user_details.objects.get(username=uname)
    except user_details.DoesNotExist:
        return Response({'error':True,
        'errors':'User Dont exist'
        }) 
    if request.method == 'GET':
        serializer=userSerializer(user)
        return Response({
            'error':False,
            'data':serializer.data
        })

@api_view(['GET'])
def get_user_by_id(request,id):
    
    try:
        user=user_details.objects.get(id=id)
    except user_details.DoesNotExist:
        return Response({'error':True,
        'errors':'User Dont exist'
        }) 
    if request.method == 'GET':
        serializer=userSerializer(user)
        return Response({
            'error':False,
            'data':serializer.data
        })



@api_view(['POST'])
def save_product(request):
    try:
        user=user_details.objects.get(username=request.POST.get('distributor'))
        serializer = productSerializer(data={ "distributor":user.id,
        "product_name":request.POST.get('product_name'),
        "price":request.POST.get('price'),
        "quantity":request.POST.get('quantity'),
        "qty_metrics":request.POST.get('qty_metrics'),
        "image":request.FILES.get('image'),
        "manufacturer":request.POST.get('manufacturer'),
        "product_category":request.POST.get('product_category'),
        }
        )
    
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'error':True,
            'errors':serializer.errors
            
            })
        return Response({
            'error':False,
            'msg':'Product Added Successfully!!'
        }) 
    except Exception as e:
        return Response({
            'error':False,
            'msg':e
        })

@api_view(['GET'])
def get_all_products(request):
    product_obj=product.objects.all()
    serializer=productSerializer(product_obj,many=True)
    return Response({
                        'error':False,
                        'data':serializer.data
                    })

@api_view(['GET'])
def get_product(request,id):
    try:
        product_obj=product.objects.get(id=id)
    except product.DoesNotExist:
        return Response({'error':True,
        'errors':'product Dont exist'
        }) 
    if request.method == 'GET':
        serializer=productSerializer(product_obj)
        return Response({
            'error':False,
            'data':serializer.data
        })

@api_view(['GET'])
def get_product_distributor(request,id):
    try:
        product_obj=product.objects.filter(distributor=id)
    except product.DoesNotExist:
        return Response({'error':True,
        'errors':'product Dont exist'
        }) 
    if request.method == 'GET':
        serializer=productSerializer(product_obj,many=True)
        return Response({
            'error':False,
            'data':serializer.data
        })
    
                    
@api_view(['GET'])
def search_product(request,pname):
    
    try:
        pro=product.objects.filter(product_name__icontains=pname).values()
        serializer=productSerializer(pro,many=True)
    except product.DoesNotExist:
        return Response({'error':True,
        'errors':'product Dont exist'
        }) 
    if pro:
        return Response({
            'error':False,
            'data':pro
        })
    else:
        return Response({
            'error':True,
            'data':serializer.data
        })



@api_view(['POST'])
def add_to_cart(request):
    try:
        obj=user_cart.objects.get(user=request.POST.get('user'),product_id=request.POST.get('product_id'))
        obj.quantity=obj.quantity+int(request.POST.get('quantity'))
        obj.price=obj.price+int(request.POST.get('price'))
        obj.save()
        pobj=product.objects.get(id=request.POST.get('product_id'))
        pobj.quantity=pobj.quantity-int(request.POST.get('quantity'))
        pobj.save()
        return Response({
        'error':False,
    }) 
    except user_cart.DoesNotExist:
        
        serializer = cartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
        'error':False,
    }) 
        else:
            return Response({'error':True,
            'errors':serializer.errors
            
            })
    
@api_view(['POST'])
def orders(request):
    DATA = {
    "amount": int(request.POST.get('price'))*100,
    "currency": "INR",
}
    razorpay_order =razorpay_client.order.create(data=DATA)
    razorpay_order_id = razorpay_order['id']
    
    
    return Response({
        'error':False,
        'razorpay_order_id' : razorpay_order_id	
    })
    

    

@api_view(['POST'])
def paymenthandler(request):	
    try:
        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id1 = request.POST.get('razorpay_order_id')
        data1={
        'razorpay_order_id':razorpay_order_id1,
        'user':request.POST.get('user'),
        'product_id':request.POST.get('product_id'),
        'distributor':request.POST.get('did'),
        'price':request.POST.get('price'),
        'quantity':request.POST.get('qty'),
        'delivery_status':"Order Confirmed",
        'payment_mode':"Online"
    }
    
        serializer = orderSerializer(data=data1)
        if serializer.is_valid():
            serializer.save()
            pobj=product.objects.get(id=request.POST.get('product_id'))
            pobj.quantity=pobj.quantity-int(request.POST.get('qty'))
            pobj.save()

        orderobj=orders_details.objects.get(razorpay_order_id=razorpay_order_id1)

        try:
            orderobj.amount_paid=True
            orderobj.save()
            data={
                'razorpay_order_id':razorpay_order_id1,
                'user':orderobj.user.id,
                'distributor':orderobj.distributor,
                'price':orderobj.price,
                'payment_id':payment_id,
                'status':True,
            }
            serializer=transactionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'error':False,
        
        })
            else:
                return Response({'error':True,
            'errors':serializer.errors
        
        })
        except Exception as e:

            # if there is an error while capturing payment.
            return Response({'error':True,
            'errors':str(e)
        })
        
    except:

        # if we don't find the required parameters in POST data
        return Response({'error':True,
           'errors':'parameter match problem'
            })
\

@api_view(['GET'])
def get_user_orders(request,id):
    try:
        order_obj=orders_details.objects.filter(user=id)
        user_obj=user_details.objects.get(id=id)
        userializer=userSerializer(user_obj)
        oserializer=orderSerializer(order_obj,many=True)
        data={}
    
        k=0	
        for champion in oserializer.data:
            proobj=product.objects.get(id=champion["product_id"])
            ps=productSerializer(proobj)
            z=ps.data
            data[k]={
            'pname':z["product_name"],
            'pimage':z["image"]
            }
            k=k+1
        return Response({
                        'error':False,
                        'data':oserializer.data,
                        'data1':userializer.data,
                        'data2':data
                    })
    except orders_details.DoesNotExist:
        return Response({
                        'error':True,
                        'errors':'no data'
                    })
    
@api_view(['GET'])
def distributor_search_product(request,pname):
    
    try:
        x=pname.split(",")
        pro=product.objects.filter(product_name__icontains=x[0],distributor=x[1]).values()
        serializer=productSerializer(pro,many=True)
    except product.DoesNotExist:
        return Response({'error':True,
        'errors':'product Dont exist'
        }) 
    if pro:
        return Response({
            'error':False,
            'data':pro
        })
    else:
        return Response({
            'error':True,
            'data':serializer.data
        })


@api_view(['POST'])
def up_product(request):
    try:
        pro=product.objects.get(id=request.POST.get('pid'))
        pro.product_name=request.POST.get('product_name')
        pro.price=request.POST.get('price')
        pro.quantity=request.POST.get('quantity')
        pro.qty_metrics=request.POST.get('qty_metrics')
        pro.image=request.FILES.get('image')
        pro.manufacturer=request.POST.get('manufacturer')
        pro.product_category=request.POST.get('product_category')
        pro.save()
        return Response({
            'error':False,
            'msg':'Product updated Successfully!!'
        }) 
    except Exception as e:
        return Response({
            'error':False,
            'msg':e
        })


@api_view(['POST'])
def up_product_data(request,id):
    try:
        pro=product.objects.get(id=id)
        pro.product_name=request.POST.get('product_name')
        pro.price=request.POST.get('price')
        pro.quantity=request.POST.get('quantity')
        pro.qty_metrics=request.POST.get('qty_metrics')
        pro.manufacturer=request.POST.get('manufacturer')
        pro.product_category=request.POST.get('product_category')
        pro.save()
        return Response({
            'error':False,
            'msg':'Product updated Successfully!!'
        }) 
    except Exception as e:
        return Response({
            'error':False,
            'msg':e
        })	
    
@api_view(['GET'])
def del_product(request,id):
    try:
        pro=product.objects.get(id=id)
        pro.delete()
        return Response({
            'error':False,
        }) 
    except Exception as e:
        return Response({
            'error':False,
            'msg':e
        })	

@api_view(['GET'])
def deliver_order(request,id):
    try:
        ord=orders_details.objects.get(razorpay_order_id=id)
        ord.is_delivered=True
        ord.delivery_status="Order Delivered"
        ord.save()
        return Response({
            'error':False,
        }) 
    except Exception as e:
        return Response({
            'error':False,
            'msg':e
        })	


@api_view(['GET'])
def get_dis_orders(request,id):
    try:
        order_obj=orders_details.objects.filter(distributor=id)
        user_obj=user_details.objects.get(id=id)
        userializer=userSerializer(user_obj)
        oserializer=orderSerializer(order_obj,many=True)
        data={}
    
        k=0	
        for champion in oserializer.data:
            proobj=product.objects.get(id=champion["product_id"])
            ps=productSerializer(proobj)
            z=ps.data
            data[k]={
            'pname':z["product_name"],
            'pimage':z["image"]
            }
            k=k+1
        return Response({
                        'error':False,
                        'data':oserializer.data,
                        'data1':userializer.data,
                        'data2':data
                    })
    except orders_details.DoesNotExist:
        return Response({
                        'error':True,
                        'errors':'no data'
                    })


@api_view(['GET'])
def get_user_transact(request,id):
    try:
        order_obj=orders_transactions.objects.filter(distributor=id)
        oserializer=transactionSerializer(order_obj,many=True)
        data={}
    
        k=0	
        for champion in oserializer.data:
            proobj=user_details.objects.get(id=champion["user"])
            proobj1=user_details.objects.get(id=champion["distributor"])
            ps1=userSerializer(proobj1)
            ps=userSerializer(proobj)
            z1=ps1.data
            z=ps.data
            data[k]={
            'pname':z["username"],
            'pimage':z1["username"]
            }
            k=k+1
        return Response({
                        'error':False,
                        'data':oserializer.data,
                        'data2':data
                    })
    except orders_transactions.DoesNotExist:
        return Response({
                        'error':True,
                        'errors':'no data'
                    })

@api_view(['GET'])
def search_transact(request,s):
    try:
        order_obj=orders_transactions.objects.filter(razorpay_order_id=s)
        oserializer=transactionSerializer(order_obj,many=True)
        data={}
    
        k=0	
        for champion in oserializer.data:
            proobj=user_details.objects.get(id=champion["user"])
            proobj1=user_details.objects.get(id=champion["distributor"])
            ps1=userSerializer(proobj1)
            ps=userSerializer(proobj)
            z1=ps1.data
            z=ps.data
            data[k]={
            'pname':z["username"],
            'pimage':z1["username"]
            }
            k=k+1
        return Response({
                        'error':False,
                        'data':oserializer.data,
                        'data2':data
                    })
    except orders_transactions.DoesNotExist:
        return Response({
                        'error':True,
                        'errors':'no data'
                    })

@api_view(['POST'])
def offlinepay(request):
    DATA = {
    "amount": int(request.POST.get('price'))*100,
    "currency": "INR",
}
    razorpay_order =razorpay_client.order.create(data=DATA)
    razorpay_order_id = razorpay_order['id']
    
    data={
                'razorpay_order_id':razorpay_order_id,
                'user':request.POST.get('user'),
                'product_id':request.POST.get('product_id'),
                'distributor':request.POST.get('did'),
                'price':request.POST.get('price'),
                'quantity':request.POST.get('qty'),
                'delivery_status':"Order Confirmed",
                'payment_mode':"Offline",
            }
    
    serializer = orderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        pobj=product.objects.get(id=request.POST.get('product_id'))
        pobj.quantity=pobj.quantity-int(request.POST.get('qty'))
        pobj.save()
        return Response({
        'error':False,
    })
    else:
        return Response({
        'error':True,
    })
    

@api_view(['POST'])
def makecomplaint(request):
    id_type=request.POST.get('id_type')
    if id_type=="Order":
        id=request.POST.get('some_id')
        try:
            obj=orders_details.objects.get(razorpay_order_id=id)
            data={
                'distributor':obj.distributor,
                'user':request.POST.get('user'),
                'its_id':id,
                'complaint_on':"Orders",
                'complaint_details':request.POST.get('msg')
            }
            serializer=complaintSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
            'error':False,
        })
        except orders_details.DoesNotExist:
            return Response({
            'error':True,
        })
    elif id_type=="Payment":
        id=request.POST.get('some_id')
        try:
            obj=orders_transactions.objects.get(razorpay_order_id=id)
            data={
                'distributor':obj.distributor,
                'user':request.POST.get('user'),
                'its_id':id,
                'complaint_on':"Payment",
                'complaint_details':request.POST.get('msg')
            }
            serializer=complaintSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
            'error':False,
        })
        except orders_details.DoesNotExist:
            return Response({
            'error':True,
        })
    elif id_type=="Product":
        id=request.POST.get('some_id')
        try:
            obj=product.objects.get(id=id)
            data={
                'distributor':obj.distributor.id,
                'user':request.POST.get('user'),
                'its_id':id,
                'complaint_on':"Product",
                'complaint_details':request.POST.get('msg')
            }
            serializer=complaintSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
            'error':False,
        })
        except orders_details.DoesNotExist:
            return Response({
            'error':True,
        })
    else:
        return Response({
        'error':True,
    })

@api_view(['POST'])
def replycomplaint(request,id):
    try:
        obj=complaints.objects.get(id=id)
        obj.reply=request.POST.get('msg')
        obj.save()
        return Response({
        'error':False,
    })
    except Exception as e:
        return Response({
        'error':True,
    })

@api_view(['GET'])
def finishcomplaint(request,id):
    try:
        obj=complaints.objects.get(id=id)
        obj.is_complaint_closed=True
        obj.save()
        return Response({
        'error':False,
    })
    except Exception as e:
        return Response({
        'error':True,
    })



@api_view(['GET'])
def getcomplaintr(request,id):
    try:
        obj=complaints.objects.filter(user=id)
        serializer=complaintSerializer(obj,many=True)
        return Response({
        'error':False,
        'data':serializer.data
    })
    except Exception as e:
        return Response({
        'error':True,
    })

@api_view(['GET'])
def getcomplaintd(request,id):
    try:
        obj=complaints.objects.filter(distributor=id)
        if(len(obj)<=0):
            return Response({
        'error':True,
    })
        serializer=complaintSerializer(obj,many=True)
        data={}
        k=0
        for i in serializer.data:
            proobj=user_details.objects.get(id=i["user"])
            ps=userSerializer(proobj)
            z=ps.data
            data[k]={
            'name':z["username"],
            }
            k=k+1
        return Response({
        'error':False,
        'data':serializer.data,
        'data1':data
        })
    except complaints.DoesNotExist:
        return Response({
        'error':True,
    })

@api_view(['GET'])
def getcartdata(request,id):
    try:
        cobj=user_cart.objects.filter(user=id)
        if(len(cobj)<=0):
            return Response({
        'error':True,
    })
        cserializer=cartSerializer(cobj,many=True)
        data1={}
        k=0
        p=0
        for i in cserializer.data:
            pobj=product.objects.get(id=i["product_id"])
            pserializer=productSerializer(pobj)
            data1[k]=pserializer.data
            p=p+i["price"]
            k=k+1
        return Response({
            'error':False,
            'data':cserializer.data,
            'data1':data1,
            'price':p
        })
    except Exception as e:
        return Response({
            'error':True
        })


@api_view(['GET'])
def deletefromcart(request,id):
    try:
        obj=user_cart.objects.get(id=id)
        obj.delete()
        return Response({
        'error':False,
    })
    except Exception as e:
        print(e)
        return Response({
        'error':True,
    })

