# Generated by Django 3.0.8 on 2020-07-13 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('item_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('icon', models.URLField()),
                ('icon_large', models.URLField()),
                ('description', models.CharField(max_length=400)),
                ('members', models.BooleanField()),
            ],
        ),
    ]
