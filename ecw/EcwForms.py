from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from ecw.models import *
from django import forms


class DepositForm(forms.ModelForm):
    trx_password = forms.CharField(label='Trx Password', required=False,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Trx Password'}))

    class Meta:
        model = DepositFunds
        fields = "__all__"
        exclude = (
            'message', 'receiversurname', 'receiverfirstname', 'status', 'banktransactionid', 'trx_batchid',
            'trx_serialid', 'created_by', 'financialtransactionid')
        widgets = {
            'bankcode': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Bank Code', 'readonly': 'readonly'}),
            'accountnumber': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Account Number', 'readonly': 'readonly'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'receiver': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiver Phone Number'}),
            'transactiontimestamp': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'transactiontimestamp', 'readonly': 'readonly'}),
            'currency': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'currency', 'readonly': 'readonly'}),

        }


class DepositFormExternal(forms.ModelForm):
    trx_password = forms.CharField(label='Trx Password', required=False,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Trx Password'}))
    class Meta:
        model = DepositFunds
        fields = "__all__"
        exclude = (
            'message', 'receiversurname', 'receiverfirstname', 'status', 'banktransactionid', 'trx_batchid',
            'trx_serialid', 'created_by', 'financialtransactionid')

        widgets = {
            'bankcode': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Bank Code', 'readonly': 'readonly'}),
            'accountnumber': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Account Number', 'readonly': 'readonly'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'receiver': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Put External ID '}),
            'transactiontimestamp': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'transactiontimestamp', 'readonly': 'readonly'}),
            'currency': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'currency', 'readonly': 'readonly'}),
            #'banktransactionid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'banktransactionid'}),
            #'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'message'}),

        }


class AccountHolderForm(forms.ModelForm):
    class Meta:
        model = AccountHolder
        fields = "__all__"
        exclude = ('firstname', 'surname', 'accountholderstatus', 'profilename')

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
        fields = (
        'operator_id', 'firstname', 'lastname', 'branch', 'email', 'is_staff', 'needs_password_change', 'group',
        'password1', 'password2',)
        widgets = {
            'operator_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'OperatorID'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'branch': forms.Select(attrs={'class': 'form-control selectpicker', 'data-size': '5',
                                          'data-live-search': 'true', 'data-style': 'btn-white'}),
            'till': forms.Select(attrs={'class': 'form-control selectpicker', 'data-size': '5',
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


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = EcwUser
        fields = ('operator_id', 'branch', 'till', 'group',)

        widgets = {
            'operator_id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'OperatorID', 'readonly': 'readonly'}),
            'branch': forms.Select(attrs={'class': 'form-control selectpicker', 'data-size': '5',
                                          'data-live-search': 'true', 'data-style': 'btn-white'}),
            'till': forms.Select(attrs={'class': 'form-control selectpicker', 'data-size': '5',
                                        'data-live-search': 'true', 'data-style': 'btn-white'}),
            'group': forms.Select(attrs={'class': 'form-control selectpicker', 'data-size': '5',
                                         'data-live-search': 'true', 'data-style': 'btn-white'}),
        }




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





class PaymentInstructionRequestForm(forms.ModelForm):
    amount_value = forms.FloatField(label='Amount', required=False,
                                    widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    transactiontimestamp_value = forms.DateTimeField(label='Transaction Timestamp', required=False,
                                                     widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    trx_password = forms.CharField(label='Trx Password', required=False,
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Trx Password'}))

    class Meta:
        model = PaymentInstructionRequest
        fields = [
            'paymentinstructionid',
            'bookingtimestamp',
            'banktransactionid',
            'response_status',
            'receiveraccountnumber',

        ]
        widgets = {

            'paymentinstructionid': forms.TextInput(attrs={'maxlength': 20, 'readonly': 'readonly'}),
            'transactionid': forms.TextInput(attrs={'maxlength': 255, 'class': 'form-control'}),
            'bookingtimestamp': forms.TextInput(
                attrs={'maxlength': 25, 'class': 'form-control', 'readonly': 'readonly'}),
            'banktransactionid': forms.TextInput(
                attrs={'maxlength': 100, 'class': 'form-control', 'readonly': 'readonly'}),
            'receiveraccountnumber': forms.TextInput(
                attrs={'maxlength': 50, 'readonly': 'readonly', 'class': 'form-control'}),
            'response_status': forms.TextInput(
                attrs={'maxlength': 50, 'class': 'form-control', 'readonly': 'readonly'}),

        }

    def __init__(self, *args, **kwargs):
        super(PaymentInstructionRequestForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['amount_value'].initial = self.instance.amount.amount
            self.fields['transactiontimestamp_value'].initial = self.instance.transactiontimestamp.timestamp


class DepositReportForm(forms.ModelForm):
    from_transactiontimestamp_value = forms.DateTimeField(label='From Transaction Timestamp', required=False,
                                                          widget=forms.TextInput(
                                                              attrs={'type': 'date', 'class': 'form-control',
                                                                     'placeholder': 'From Transaction Timestamp'}))
    to_transactiontimestamp_value = forms.DateTimeField(label='To Transaction Timestamp', required=False,
                                                        widget=forms.TextInput(
                                                            attrs={'type': 'date', 'class': 'form-control',
                                                                   'placeholder': 'To Transaction Timestamp'}))

    class Meta:
        model = PaymentInstructionRequest
        fields = [

        ]
        exclude = (
            'receiversurname', 'receiverfirstname', 'status', 'banktransactionid', 'trx_batchid', 'trx_serialid',
            'message')

    def __init__(self, *args, **kwargs):
        super(DepositReportForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['from_transactiontimestamp_value'].initial = self.instance.transactiontimestamp.timestamp
            self.fields['to_transactiontimestamp_value'].initial = self.instance.transactiontimestamp.timestamp


class WithdrawReportForm(forms.ModelForm):
    from_transactiontimestamp_value = forms.DateTimeField(label='From Transaction Timestamp', required=False,
                                                          widget=forms.TextInput(
                                                              attrs={'type': 'date', 'class': 'form-control',
                                                                     'placeholder': 'From Transaction Timestamp'}))
    to_transactiontimestamp_value = forms.DateTimeField(label='To Transaction Timestamp', required=False,
                                                        widget=forms.TextInput(
                                                            attrs={'type': 'date', 'class': 'form-control',
                                                                   'placeholder': 'To Transaction Timestamp'}))

    class Meta:
        model = PaymentInstructionRequest
        fields = [

        ]
        exclude = (
            'receiversurname', 'receiverfirstname', 'status', 'banktransactionid', 'trx_batchid', 'trx_serialid',
            'message')

    def __init__(self, *args, **kwargs):
        super(WithdrawReportForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['from_transactiontimestamp_value'].initial = self.instance.transactiontimestamp.timestamp
            self.fields['to_transactiontimestamp_value'].initial = self.instance.transactiontimestamp.timestamp
