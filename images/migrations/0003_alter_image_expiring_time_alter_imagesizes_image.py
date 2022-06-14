# Generated by Django 4.0.5 on 2022-06-12 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='expiring_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='imagesizes',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_sizes', to='images.image'),
        ),
    ]