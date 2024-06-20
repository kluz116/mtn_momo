from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.utils import timezone
from datetime import datetime
from django.db import models
from .managers import CustomUserManager


# Create your models here.
class DepositFunds(models.Model):
    deposists_to = [("phone_number", "PhoneNumber (Msisdn)"), ("external_id", "External ID"), ]
    bankcode = models.CharField(max_length=30, null=False, default=37)
    accountnumber = models.CharField(max_length=15, blank=True, null=True, default='20680300000')
    amount = models.FloatField(max_length=15, null=False, blank=False)
    receiver = models.CharField(max_length=35)
    transactiontimestamp = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    currency = models.CharField(max_length=5, blank=False, null=False, default='UGX')
    banktransactionid = models.CharField(max_length=15, null=False, blank=False)
    message = models.CharField(max_length=50, null=False, blank=False)
    receiverfirstname = models.CharField(max_length=50, null=False, blank=False)
    receiversurname = models.CharField(max_length=50, null=False, blank=False)
    status = models.CharField(max_length=50, null=False, blank=False)
    trx_batchid = models.CharField(max_length=50, null=False, blank=False)
    trx_serialid = models.CharField(max_length=50, null=False, blank=False)


class AccountHolder(models.Model):
    firstname = models.CharField(max_length=50, null=False, blank=False)
    surname = models.CharField(max_length=50, null=False, blank=False)
    msisdn = models.CharField(max_length=50, null=False, blank=False)
    accountholderstatus = models.CharField(max_length=50, null=False, blank=False)
    profilename = models.CharField(max_length=50, null=False, blank=False)


class TransactionTimestamp(models.Model):
    timestamp = models.CharField(max_length=100)


class Amount(models.Model):
    amount = models.FloatField()
    currency = models.CharField(max_length=3)


class PaymentInstructionRequest(models.Model):
    transactiontimestamp = models.OneToOneField(TransactionTimestamp, on_delete=models.CASCADE)
    amount = models.OneToOneField(Amount, on_delete=models.CASCADE)
    paymentinstructionid = models.CharField(max_length=20)
    receiverbankcode = models.CharField(max_length=20)
    receiveraccountnumber = models.CharField(max_length=20)
    receiverfirstname = models.CharField(max_length=50)
    receiversurname = models.CharField(max_length=50)
    message = models.CharField(max_length=255)
    transmissioncounter = models.CharField(max_length=255, null=True)
    transactionid = models.CharField(max_length=255, null=True)
    bookingtimestamp = models.CharField(max_length=25,blank=True,null=True)
    banktransactionid = models.CharField(max_length=25,null=True,blank=True)
    random_challenge = models.CharField(max_length=50,blank=True,null=True)
    response_status = models.CharField(max_length=50,blank=True,null=True,default='PENDING')


class Xsignature(models.Model):
    x_signature = models.TextField(blank=True, null=True)
    paymentinstructionid = models.CharField(max_length=35)


class Branch(models.Model):
    name = models.CharField(max_length=20)
    branch_code = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class EcwGroup(Group):
    #name = models.CharField(max_length=100)
    description = models.TextField(blank=True)




class EcwUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    firstname = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    #group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(EcwGroup, on_delete=models.CASCADE,blank=True, null=True)
    needs_password_change = models.BooleanField(default=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f' {self.username}'