# Generated by Django 3.2.5 on 2021-08-01 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=256, null=True, verbose_name='ステータス')),
                ('num', models.PositiveIntegerField(blank=True, null=True, verbose_name='個数')),
                ('curr', models.BooleanField(blank=True, default=False, null=True, verbose_name='今回分か否か')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='オーダー発生時刻')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.nonloginuser')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant.menu')),
            ],
        ),
        migrations.CreateModel(
            name='NomihoOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=256, null=True, verbose_name='ステータス')),
                ('table', models.PositiveIntegerField(blank=True, null=True, verbose_name='テーブル番号')),
                ('num', models.PositiveIntegerField(blank=True, null=True, verbose_name='人数')),
                ('curr', models.BooleanField(blank=True, default=False, null=True, verbose_name='今回分か否か')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='飲み放題開始時刻')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.nonloginuser')),
                ('nomiho', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant.nomiho')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.PositiveIntegerField(blank=True, null=True, verbose_name='個数')),
                ('curr', models.BooleanField(blank=True, default=False, null=True, verbose_name='今回分か否か')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='カート追加時刻')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.nonloginuser')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant.menu')),
            ],
        ),
    ]
