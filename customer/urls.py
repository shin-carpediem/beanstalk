from django.urls import path
from . import views


app_name = 'customer'
urlpatterns = [
    path('', views.index, name='index'),
    path('table/', views.table, name='table'),
    path('waiting/', views.waiting, name='waiting'),
    path('waiting/admin/', views.waiting_admin, name='waiting_admin'),
    path('judge/', views.judge, name='judge'),
    path('allowing/', views.allowing, name='allowing'),
    path('deny/', views.deny, name='deny'),
    path('denied/', views.denied, name='denied'),
    path('menu/', views.menu, name='menu'),
    path('<int:category_id>/filter/', views.filter, name='filter'),
    path('<int:menu_id>/detail/', views.menu_detail, name='menu_detail'),
    path('<int:menu_id>/detail/request/', views.request, name='request'),
    path('cart/', views.cart, name='cart'),
    path('cart/static/', views.cart_static, name='cart_static'),
    path('cart/<int:menu_id>/detail/', views.cart_detail, name='cart_detail'),
    path('cart/cart_ch/', views.cart_ch, name='cart_ch'),
    path('order/', views.order, name='order'),
    path('nomiho/<int:nomiho_id>', views.nomiho, name='nomiho'),
    path('history/', views.history, name='history'),
    path('thanks/', views.thanks, name='thanks'),
    path('stop/', views.stop, name='stop'),
]
