# Generated by Django 5.0.2 on 2024-02-11 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('SKU', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('in_stock', models.IntegerField()),
                ('available_stock', models.IntegerField()),
            ],
        ),
    ]