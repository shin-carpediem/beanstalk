# Generated by Django 3.2.5 on 2021-08-01 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.CharField(blank=True, max_length=256, null=True, verbose_name='アレルギー食品')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='作成日')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='カテゴリ')),
                ('nomiho', models.BooleanField(blank=True, default=False, null=True, verbose_name='飲み放題用カテゴリ')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='作成日')),
            ],
        ),
        migrations.CreateModel(
            name='Nomiho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='飲み放題プラン名')),
                ('price', models.PositiveIntegerField(blank=True, null=True, verbose_name='価格')),
                ('duration', models.PositiveIntegerField(blank=True, null=True, verbose_name='制限時間（分）')),
                ('comment', models.CharField(blank=True, max_length=256, null=True, verbose_name='一押しポイント')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='作成日')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='表示名')),
                ('price', models.PositiveIntegerField(blank=True, null=True, verbose_name='価格')),
                ('img', models.ImageField(blank=True, null=True, upload_to='img', verbose_name='イメージ画像')),
                ('chef_img', models.ImageField(blank=True, null=True, upload_to='chef_img', verbose_name='シェフの顔写真')),
                ('comment', models.TextField(blank=True, max_length=500, null=True, verbose_name='コメント')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='作成日')),
                ('allergies', models.ManyToManyField(blank=True, null=True, to='restaurant.Allergy')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.category')),
            ],
        ),
    ]
