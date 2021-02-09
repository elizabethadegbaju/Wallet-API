from rest_framework import serializers

from .models import Transaction, Wallet


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'type', 'value', 'created_at']


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'user', 'balance']
