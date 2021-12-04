from django.urls import path
from . import views
from .middleware.auth import auth_middleware
urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    path('signup/', views.signup, name='signuppage'),
    path('login/', views.LoginView.as_view(), name='loginpage' ),
    path('logout/', views.logout, name='logoutpage'),
    path('cart/', views.cartView.as_view(), name='cartpage'),
    path('check-out/', views.checkoutView.as_view(), name='checkOut'),
    # path('orders/', views.orderView.as_view(), name='orderpage'),
    path('orders/', auth_middleware(views.orderView.as_view()), name='orderpage'),



]