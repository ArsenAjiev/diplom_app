# Generated by Django 3.2.7 on 2021-11-10 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20211110_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='постер'),
        ),
    ]