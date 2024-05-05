# Generated by Django 5.0.3 on 2024-05-02 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_work2nonlitigation_finished_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='work2nonlitigation',
            name='case_stage',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='work2nonlitigation',
            name='details',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='workligitation',
            name='details',
            field=models.TextField(null=True),
        ),
        migrations.DeleteModel(
            name='WorkNonLitigation',
        ),
    ]
