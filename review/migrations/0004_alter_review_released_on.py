# Generated by Django 3.2.18 on 2023-03-22 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_rename_producer_review_director'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='released_on',
            field=models.DateField(),
        ),
    ]