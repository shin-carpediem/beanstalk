# Generated by Django 3.1.6 on 2021-05-30 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logo',
            field=models.ImageField(blank=True, max_length=50, null=True, upload_to='logo', verbose_name='ロゴ'),
        ),
    ]
