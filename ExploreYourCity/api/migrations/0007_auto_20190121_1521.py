# Generated by Django 2.1.5 on 2019-01-21 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_player_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='mission',
            name='value',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
