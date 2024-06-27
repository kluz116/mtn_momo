from django.urls import path
#import ecw.views as views
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.login_request, name='login'),
    path("logout_request_metropol", views.logout_request_metropol, name="logout_request_metropol"),
    path('getIndex', views.getIndex, name='getIndex'),
    path('addDeposit', views.addDeposit, name='addDeposit'),
    path('addAccountHolder', views.addAccountHolder, name='addAccountHolder'),
    path('getDeposits', views.getDeposits, name='getDeposits'),
    path('getAccountHolders', views.getAccountHolders, name='getAccountHolders'),
    path('addDepositExternalId', views.addDepositExternalId, name='addDepositExternalId'),
    path('paymentinstruction', views.paymentInstruction, name='paymentInstruction'),
    path('getPaymentInstructions', views.getPaymentInstructions, name='getPaymentInstructions'),
    path('PaymentInstructionsDetail/<int:id>/', views.PaymentInstructionsDetail, name='PaymentInstructionsDetail'),
    path('generate_excel', views.generate_excel, name='generate_excel'),
    path('generate_excel_withdraw', views.generate_excel_withdraw, name='generate_excel_withdraw'),
    path('addBranch', views.addBranch, name='addBranch'),
    path('getBranches', views.getBranches, name='getBranches'),
    path('addUsers', views.addUsers, name='addUsers'),

]
