# Generated by Django 4.0.5 on 2022-06-15 16:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('expiring_time', models.IntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('image_expiring', models.BinaryField(blank=True, editable=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImageSizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(upload_to='images/')),
                ('height', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_sizes', to='images.image')),
            ],
        ),
    ]
