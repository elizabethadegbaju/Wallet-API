import time

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label) -> bool:
        """Does the user have permissions to view the app `app_label`?"""
        return True

    @property
    def is_staff(self) -> bool:
        """Is the user a member of staff?"""
        return self.is_admin


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('D', 'Deposit'),
        ('W', 'Withdraw')
    ]

    id = models.CharField(max_length=20, primary_key=True)
    wallet = models.ForeignKey(to='Wallet', on_delete=models.CASCADE)
    type = models.CharField(choices=TRANSACTION_TYPE, max_length=20)
    value = models.DecimalField(decimal_places=2, max_digits=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_at} Reference No. {self.id}'

    class Meta:
        ordering = ['-created_at']


class Wallet(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    # user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, default=0, max_digits=20)
    name = models.CharField(max_length=255)

    def withdraw(self, amount):
        self.balance -= amount
        transaction_id = int(round(time.time() * 1000))
        transaction = Transaction.objects.create(id=transaction_id,
                                                 wallet=self, type='W',
                                                 value=amount)
        self.save()
        transaction.save()

    def deposit(self, amount):
        self.balance += amount
        transaction_id = int(round(time.time() * 1000))
        transaction = Transaction.objects.create(id=transaction_id,
                                                 wallet=self, type='D',
                                                 value=amount)
        self.save()
        transaction.save()

    def __str__(self):
        return f'({self.id}) {self.name}'
