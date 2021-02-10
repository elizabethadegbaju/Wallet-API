from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from app.models import User
from app.serializers import *


@login_required
@api_view(('GET',))
@renderer_classes((JSONRenderer,))
@csrf_exempt
def api_transaction_history(request):
    """
    List all transactions of logged in user.

    :param request:
    :return: JSON Response:
    """
    transactions = Transaction.objects.filter(wallet__user=request.user)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(data=serializer.data)


@login_required
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@csrf_exempt
def api_fund_wallet(request):
    data = JSONParser().parse(request)
    amount = data['amount']
    wallet_id = str(data['wallet'])
    wallet = Wallet.objects.get(id=wallet_id)
    wallet.deposit(amount)
    wallet.save()

    return Response(status=200,
                    data={
                        'success': f'Wallet with ID {wallet_id} was successfully funded with {amount}'})


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@csrf_exempt
def api_create_account(request):
    data = JSONParser().parse(request)
    email = data['email']
    password = data['password']
    user = User.objects.create_user(email, password)
    user.save()
    return Response(status=201,
                    data={'success', 'Account created successfully!'})


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@csrf_exempt
def api_login(request):
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


@login_required
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@csrf_exempt
def api_create_wallet(request):
    data = JSONParser().parse(request)
    name = data['name']
    user = request.user
    today = now().date()
    wallet_id = f'{user.id}0{today.toordinal()}'
    wallet = Wallet.objects.create(user=user, name=name, id=wallet_id)
    wallet.save()
    return Response(status=201, data={'success': f'Wallet created ({name})'})


@login_required
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@csrf_exempt
def api_transfer_funds(request):
    data = JSONParser().parse(request)
    from_wallet_id = data['from_wallet']
    to_wallet_id = data['to_wallet']
    amount = data['amount']
    user = request.user
    from_wallet = Wallet.objects.get(id=from_wallet_id)
    to_wallet = Wallet.objects.get(id=to_wallet_id)
    if from_wallet in user.wallet_set:
        from_wallet.withdraw(amount)
        to_wallet.deposit(amount)
        from_wallet.save()
        to_wallet.save()
        return Response(status=200, data={'success': 'Transfer successful!'})
    else:
        return Response(status=403, data={
            'error': 'Permission Denied. You cannot transfer from this wallet.'})
