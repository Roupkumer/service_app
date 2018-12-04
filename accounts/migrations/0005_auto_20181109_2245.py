# Generated by Django 2.1 on 2018-11-09 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_server_avg_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='s',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='s', to='accounts.Server'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_voted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='server',
            name='avg_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
