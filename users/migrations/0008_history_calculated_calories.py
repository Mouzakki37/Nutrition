# Generated by Django 4.2.1 on 2023-08-11 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile_delete_frgt'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='calculated_calories',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]