# Generated by Django 3.2.5 on 2021-07-19 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='curr',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='今回分か否か'),
        ),
        migrations.AddField(
            model_name='order',
            name='curr',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='今回分か否か'),
        ),
    ]