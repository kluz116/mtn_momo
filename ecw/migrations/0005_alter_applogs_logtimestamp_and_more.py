# Generated by Django 4.2.13 on 2024-06-28 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecw', '0004_alter_applogs_logtimestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applogs',
            name='logtimestamp',
            field=models.DateTimeField(default='2024-06-28T15:54:35'),
        ),
        migrations.AlterField(
            model_name='depositfunds',
            name='transactiontimestamp',
            field=models.DateTimeField(default='2024-06-28T15:54:35'),
        ),
        migrations.AlterField(
            model_name='paymentinstructionrequest',
            name='receiveraccountnumber',
            field=models.CharField(max_length=100),
        ),
    ]