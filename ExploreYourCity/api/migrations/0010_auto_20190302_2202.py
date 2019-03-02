# Generated by Django 2.1.7 on 2019-03-02 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20190202_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='missions',
        ),
        migrations.AddField(
            model_name='player',
            name='missions_active',
            field=models.ManyToManyField(blank=True, related_name='_player_missions_active_+', to='api.Mission'),
        ),
        migrations.AddField(
            model_name='player',
            name='missions_completed',
            field=models.ManyToManyField(blank=True, related_name='_player_missions_completed_+', to='api.Mission'),
        ),
        migrations.AddField(
            model_name='player',
            name='objectives_active',
            field=models.ManyToManyField(blank=True, related_name='_player_objectives_active_+', to='api.Objective'),
        ),
        migrations.AlterField(
            model_name='player',
            name='objectives_completed',
            field=models.ManyToManyField(blank=True, related_name='_player_objectives_completed_+', to='api.Objective'),
        ),
    ]