# Generated by Django 5.0.6 on 2024-06-22 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MoneyMinderApp', '0007_alter_budget_amount_alter_expense_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Saving',
            new_name='Savings',
        ),
    ]
