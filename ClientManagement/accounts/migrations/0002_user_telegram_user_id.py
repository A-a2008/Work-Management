# Generated by Django 5.0.3 on 2024-05-09 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_user_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
