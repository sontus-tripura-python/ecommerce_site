import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_item_total_price':0, 'get_total_item': 0, 'shipping':False }
    cartItems =  order['get_total_item']
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            order['get_item_total_price'] += total
            order['get_total_item'] += cart[i]["quantity"]
            item = {
                'product':{
                    'id': product.id,
                    'product_name':product.product_name,
                    'price':product.price,
                    'product_image': product.product_image
                },
                'quantity':cart[i]['quantity'],
                'get_total': total,
            }

            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems': cartItems, 'items': items, 'order': order}



def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems =  order.get_total_item
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'items': items, 'order': order}


