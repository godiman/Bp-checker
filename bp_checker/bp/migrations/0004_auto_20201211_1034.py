# Generated by Django 3.1.3 on 2020-12-11 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bp', '0003_auto_20201211_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('phone_no', models.CharField(max_length=11)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('password', models.CharField(max_length=254)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
