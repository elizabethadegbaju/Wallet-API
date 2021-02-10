"""WalletAPI.app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from app import views

urlpatterns = [
    path('register/', views.api_create_account, name='register'),
    path('login/', views.api_login, name='login'),
    path('fund-wallet/', views.api_fund_wallet, name='fund-wallet'),
    path('create-wallet/', views.api_create_wallet, name='create-wallet'),
    path('transfer-funds/', views.api_transfer_funds, name='transfer-funds'),
    path('transaction-history', views.api_transaction_history,
         name='transaction-history')
]
