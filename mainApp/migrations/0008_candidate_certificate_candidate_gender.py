# Generated by Django 4.2.7 on 2025-03-30 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_remove_staff_email_remove_staff_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='certificate',
            field=models.FileField(blank=True, null=True, upload_to='certificates/'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=50),
        ),
    ]
