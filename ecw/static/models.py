from django.contrib.auth.models import User,Group
from django.db import models
from dateutil.relativedelta import relativedelta
from datetime import *
from django_currentuser.db.models import CurrentUserField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from AutomationApps import settings
from .managers import CustomUserManager


class Branch(models.Model):
    name = models.CharField(max_length=20)
    branch_code = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class CustomGroup(Group):
    #name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    firstname = models.CharField(max_length=50,blank=True)
    lastname = models.CharField(max_length=50,blank=True)
    #password1 = models.CharField(max_length=50, blank=True)
    #password2 = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f' {self.firstname} {self.lastname}'


class SecurityType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SecurityStatus(models.Model):
    name = models.CharField(max_length=100)
    security_type = models.ForeignKey(SecurityType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LandTitleType(models.Model):
    name = models.CharField(max_length=100)
    security_type = models.ForeignKey(SecurityType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Customer(models.Model):
    gender_list = [("M", "M"), ("F", "F"), ]
    customer_status = [("No", "No"), ("Yes", "Yes"), ]
    firstname = models.CharField(max_length=60)
    middlename = models.CharField(max_length=60, blank=True, null=True)
    lastname = models.CharField(max_length=60)
    gender = models.CharField(max_length=10, choices=gender_list)
    status = models.CharField(max_length=5, choices=customer_status, default='No')
    national_id = models.CharField(max_length=15, blank=True, null=True)
    bank_account = models.CharField(max_length=20, blank=True)
    bank_tin = models.CharField(max_length=20, null=True)
    created_on = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.middlename}'


class Security(models.Model):
    client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    client_type = models.CharField(max_length=50, choices=[("borrower", "Borrower"), ("Third_Party", "Third Party")])
    status = models.CharField(max_length=50,
                              choices=[("InCustody", "In Custody"), ("Withdrawn", "Withdrawn"), ("Expired", "Expired"),
                                       ("Recieved", "Recieved")], default='InCustody')
    security_file = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True)
    Security_owner = models.CharField(max_length=20)
    security_type = models.ForeignKey(SecurityType, on_delete=models.CASCADE)
    security_status = models.ForeignKey(SecurityStatus, on_delete=models.CASCADE)
    LandTitleType = models.ForeignKey(LandTitleType, on_delete=models.CASCADE)
    LeaseHoldStartDate = models.DateField(blank=True, null=True)
    Lease_Hold_Tenure = models.IntegerField(blank=True, null=True)
    # LeaseHoldExpiryDate = models.DateField()
    # DateRecieved = models.DateField()
    # ForcedSaleValue = models.CharField(max_length=100)
    Security_Description = models.CharField(max_length=100)
    # Insurance_Details = models.CharField(max_length=100,blank=True)
    withdrawn_on = models.DateField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)
    # created_by = CurrentUserField()
    sent_for_mortgaging_by = CurrentUserField(related_name='sent_for_mortgaging_by')
    sent_for_mortgaging_at = models.DateField(default=datetime.now)
    sent_for_further_charge_by = CurrentUserField(related_name='sent_for_further_charge_by')
    sent_for_further_charge_at = models.DateField(default=datetime.now)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def lease_end_date(self):
        if self.LeaseHoldStartDate is None:
            return None
        else:
            return self.LeaseHoldStartDate + relativedelta(years=self.Lease_Hold_Tenure)

    def save(self, *args, **kwargs):
        if not self.pk:
            Customer.objects.filter(pk=self.client_id).update(status='Yes')
        super().save(*args, **kwargs)


class Contracts(models.Model):
    Party_Name = models.CharField(max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    Contract_value = models.FloatField(max_length=20)
    DateSigned = models.DateField(default=datetime.now)
    Duration = models.CharField(max_length=20)
    status = models.CharField(max_length=50, choices=[("on", "On"), ("Expired", "Expired"), ("Expired", "Expired"),
                                                      ("Terminated", "Terminated")], default='on')
    Expiry_Date = models.DateField(default=datetime.now)
    Description = models.CharField(max_length=200)
    Compulsory_Terms = models.CharField(max_length=200)
    InsuranceTerms = models.CharField(max_length=200)
    contract_file = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=datetime.now)
