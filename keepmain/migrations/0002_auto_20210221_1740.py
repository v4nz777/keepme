# Generated by Django 3.0.8 on 2021-02-21 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepmain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionborrow',
            name='promised_return',
            field=models.DateField(),
        ),
    ]
