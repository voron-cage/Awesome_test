# Generated by Django 3.0.7 on 2020-06-22 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_uploads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photocache',
            name='height',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='photocache',
            name='size',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='photocache',
            name='width',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
