# Generated by Django 3.0.8 on 2021-02-21 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepmain', '0003_auto_20210221_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outcome',
            name='promised_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='return_date_attempt',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='outcome',
            name='return_date_success',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='thing',
            name='promised_return_by_borrower',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transactionborrow',
            name='promised_return',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='transactionlend',
            name='promised_return',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='transactionreturn',
            name='date_returned',
            field=models.DateField(blank=True, null=True),
        ),
    ]