from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from ecw.models import *
from django import forms


class DepositForm(forms.ModelForm):
    class Meta:
        model = DepositFunds
        fields = "__all__"
        exclude = ('receiversurname', 'receiverfirstname', 'status', 'banktransactionid', 'trx_batchid', 'trx_serialid')
        widgets = {
            'bankcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Code'}),
            'accountnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Number'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'receiver': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiver Phone Number'}),
            'transactiontimestamp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'transactiontimestamp'}),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'currency'}),
            #'banktransactionid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'banktransactionid'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'message'}),

        }

class DepositFormExternal(forms.ModelForm):
    class Meta:
        model = DepositFunds
        fields = "__all__"
        exclude = ( 'receiversurname', 'receiverfirstname','status','banktransactionid','trx_batchid','trx_serialid')

        widgets = {
            'bankcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Code'}),
            'accountnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Number'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'receiver': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Put External ID '}),
            'transactiontimestamp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'transactiontimestamp'}),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'currency'}),
            #'banktransactionid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'banktransactionid'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'message'}),

        }

class AccountHolderForm(forms.ModelForm):
    class Meta:
        model = AccountHolder
        fields = "__all__"
        exclude = ('firstname', 'surname','accountholderstatus','profilename')


        widgets = {
            'msisdn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),


        }


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

    class Meta:
        model = EcwUser
        fields = ('username','firstname', 'lastname', 'branch', 'email', 'is_staff','needs_password_change', 'group', 'password1', 'password2',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'branch': forms.Select(attrs={'class': 'form-control selectpicker', 'data-size': '5',
                                          'data-live-search': 'true', 'data-style': 'btn-white'}),
            'group': forms.Select(attrs={'class': 'form-control selectpicker', 'data-size': '5',
                                         'data-live-search': 'true', 'data-style': 'btn-white'}),
        }

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomGroupForm(forms.ModelForm):
    class Meta:
        model = EcwGroup
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = EcwUser
        fields = ("email",)


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = "__all__"
        widgets = {
            'branch_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Branch Code'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Branch Name'}),
        }



class PaymentForm(forms.Form):
    pass