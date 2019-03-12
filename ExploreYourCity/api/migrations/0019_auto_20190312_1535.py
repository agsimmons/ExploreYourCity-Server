# Generated by Django 2.1.7 on 2019-03-12 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_remove_player_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_from', to='api.Player')),
                ('request_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_to', to='api.Player')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='request',
            unique_together={('request_from', 'request_to')},
        ),
    ]
