import datetime
from decimal import Decimal

from django.contrib.auth import authenticate, login
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from app.models import User
from app.serializers import *


@api_view(('GET',))
@authentication_classes([BasicAuthentication])
def api_transaction_history(request):
    """
    get: Retrieves the transaction history in reverse
    chronological order
    """
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True,
                                       context={'request': request})
    return Response(data=serializer.data)


@api_view(('POST',))
@authentication_classes([BasicAuthentication])
def api_fund_wallet(request):
    """
    post: Deposit funds into specified wallet.
    """
    data = JSONParser().parse(request)
    amount = Decimal(data['amount'])
    try:
        wallet_id = str(data['wallet_id'])
        wallet = Wallet.objects.get(id=wallet_id)
        wallet.deposit(amount)
        wallet.save()
        return Response(status=200, data={
            'success': f'Wallet with ID {wallet_id} was successfully funded with {amount}'})
    except Wallet.DoesNotExist:
        return Response(status=404,
                        data={'error': f'Wallet with matching ID not found'})


@api_view(('POST',))
@authentication_classes([BasicAuthentication])
def api_create_account(request):
    """
    post: Create user account with specified details.
    """
    data = JSONParser().parse(request)
    email = data['email']
    password = data['password']
    user = User.objects.create_user(email, password)
    user.save()
    return Response(status=201,
                    data={'success', 'Account created successfully!'})


@api_view(('POST',))
@authentication_classes([BasicAuthentication])
def api_login(request):
    """
    post: Log in user with specified details.
    """
    data = JSONParser().parse(request)
    email = data['email']
    password = data['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return Response(status=200,
                        data={'success', f'User {email} logged in.'})
    else:
        return Response(status=404,
                        data={'error', f'User {email} not found.'})


@api_view(('POST',))
@authentication_classes([BasicAuthentication])
def api_create_wallet(request):
    """
    post: Create a wallet with the given name and return the new wallet's ID.
    """
    data = JSONParser().parse(request)
    name = data['name']
    wallet_id = f'{int(datetime.datetime.utcnow().timestamp())}'
    wallet = Wallet.objects.create(name=name, id=wallet_id)
    wallet.save()
    return Response(status=201, data={'success': f'Wallet created ({name}). '
                                                 f'Wallet ID  is '
                                                 f'{wallet_id}.'})


@api_view(('POST',))
@authentication_classes([BasicAuthentication])
def api_transfer_funds(request):
    """
    post: Transfers funds from one wallet to the other and creates the
    related transaction logs.
    """
    data = JSONParser().parse(request)
    from_wallet_id = data['from_wallet']
    to_wallet_id = data['to_wallet']
    amount = Decimal(data['amount'])
    try:
        from_wallet = Wallet.objects.get(id=from_wallet_id)
        to_wallet = Wallet.objects.get(id=to_wallet_id)
        from_wallet.withdraw(amount)
        to_wallet.deposit(amount)
        from_wallet.save()
        to_wallet.save()
        return Response(status=200, data={'success': 'Transfer successful!'})
    except Wallet.DoesNotExist:
        return Response(status=404,
                        data={'error': f'Wallet with matching ID not found'})
