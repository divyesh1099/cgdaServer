# Generated by Django 4.2.4 on 2023-08-14 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_billorder_buyergstn_alter_billorder_deductions_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billorder',
            name='buyerGstn',
        ),
        migrations.RemoveField(
            model_name='billorder',
            name='deductions',
        ),
        migrations.RemoveField(
            model_name='billorder',
            name='vendorGstStatus',
        ),
        migrations.RemoveField(
            model_name='billorder',
            name='vendorGstn',
        ),
    ]
