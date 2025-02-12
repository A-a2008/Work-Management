# Generated by Django 5.0.3 on 2024-05-09 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_paymentslitigation_date_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentslitigation',
            name='total_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='paymentsnonlitigation',
            name='total_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='paymentsnonlitigation',
            name='amount_paid',
            field=models.IntegerField(default=0),
        ),
    ]
