# Generated by Django 4.2.13 on 2024-06-20 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecw', '0006_alter_depositfunds_transactiontimestamp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingTimestamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='depositfunds',
            name='transactiontimestamp',
            field=models.DateTimeField(default='2024-06-20T18:36:02'),
        ),
        migrations.AlterField(
            model_name='paymentinstructionrequest',
            name='banktransactionid',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='PaymentInstructionResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, default='PENDING', max_length=50, null=True)),
                ('paymentinstructionid', models.CharField(max_length=20)),
                ('banktransactionid', models.CharField(blank=True, max_length=25, null=True)),
                ('amount', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ecw.amount')),
                ('bookingtimestamp', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ecw.bookingtimestamp')),
                ('transactiontimestamp', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ecw.transactiontimestamp')),
            ],
        ),
    ]
