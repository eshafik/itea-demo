# Generated by Django 3.0.2 on 2020-01-22 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0003_auto_20200122_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensetransaction',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='incometransaction',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]