# Generated by Django 4.2.13 on 2024-06-20 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecw', '0007_bookingtimestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositfunds',
            name='banktransactionid',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='depositfunds',
            name='transactiontimestamp',
            field=models.DateTimeField(default='2024-06-20T18:37:22'),
        ),
        migrations.AlterField(
            model_name='paymentinstructionresponse',
            name='banktransactionid',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]