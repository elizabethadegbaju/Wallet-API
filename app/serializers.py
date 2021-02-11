from rest_framework import serializers

from .models import Transaction, Wallet


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'balance']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    wallet = WalletSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'type', 'value', 'created_at']
