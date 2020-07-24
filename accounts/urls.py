from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('membership/', views.membership, name='membership'),
    path('products/', views.products, name='products'),

    path('', views.homePage, name='home'),
    path('user/', views.userPage, name='user-page'),
    path('user/settings/', views.accountSettings, name='account_settings'),
    path('user/reservation/', views.makeReservation, name='make_reserv'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('customers/', views.allCustomer, name='customers'),
    path('orders/', views.allOrder, name='orders'),
    path('inventory/', views.inventory, name='inventory'),
    path('orders/pending/', views.pendingOrders, name='pending'),
    path('orders/reserved/', views.reservedOrders, name='reserved'),
    path('orders/in-use/', views.inUseOrders, name='in-use'),
    path('orders/total-sales/', views.totalSales, name='total-sales'),
    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

    path('reset_password/',
      auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
      name="reset_password"),
    path('reset_password_sent/',
      auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
      name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
      auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
      name="password_reset_confirm"),
    path('reset_password_complete/',
      auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
      name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
