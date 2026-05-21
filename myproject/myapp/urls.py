from django.urls import path
from . import views

urlpatterns=[
             path('',views.home,name='home'),
             path('signup/',views.signup,name='signup'),
             path('login/',views.login,name='login'),
             path('logout/',views.logout,name='logout'),
             path('product_detail/',views.product_detail,name='product_detail'),
             path('addtocart/',views.addtocart,name='addtocart'),
             path('cart_item/',views.cart_item,name='cart_item'),
             path('update_quantity/',views.update_quantity,name='update_quantity'),
             path('check_out/',views.check_out,name='check_out'),
             path('order_form/',views.order_form,name='order_form'),
             path('orders_page/',views.orders_page,name='orders_page')
            ]