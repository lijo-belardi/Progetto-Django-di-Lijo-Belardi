# Generated by Django 3.2.8 on 2021-10-14 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210611_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
