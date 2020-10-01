from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
       path('', views.product_list, name='product_list'),
      # path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
       path('product-details', views.product_details, name='product_details'),
       path('checkout/', views.checkout, name='checkout_list'),
       path('cart', views.cart_list, name='cart_list'),
       path('update_item/', views.updateItem, name='update_item'),
        path('process_order/', views.proceOrder, name='process_order'),
    path ('username-valid/', csrf_exempt(views.usernameValidation), name='username-valid'),
    path('email-validation/', csrf_exempt(views.emailValidation), name='email-validation'),
]
