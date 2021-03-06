# Generated by Django 3.0.2 on 2020-01-22 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0005_auto_20200122_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensetransaction',
            name='expense_date',
            field=models.DateTimeField(blank=True, db_index=True, help_text='YYYY-MM-DD', null=True),
        ),
        migrations.AlterField(
            model_name='incometransaction',
            name='received_date',
            field=models.DateTimeField(blank=True, db_index=True, help_text='YYYY-MM-DD', null=True),
        ),
    ]
