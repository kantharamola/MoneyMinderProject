# Generated by Django 5.0.6 on 2024-06-24 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MoneyMinderApp', '0009_auto_20240624_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('food', 'Food'), ('transport', 'Transport'), ('entertainment', 'Entertainment'), ('utilities', 'Utilities'), ('others', 'Others'), ('unimportant', 'Unimportant')], max_length=50),
        ),
    ]
