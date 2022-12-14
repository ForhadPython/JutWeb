# Generated by Django 3.2 on 2022-02-20 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skilldun', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Founder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='static/media/founder/')),
                ('name', models.CharField(max_length=40)),
                ('designations', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=400)),
                ('priority', models.IntegerField(default=1)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
