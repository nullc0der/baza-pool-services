# Generated by Django 3.0.2 on 2020-09-25 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tokendb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VotingSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('minimum_amount_per_token', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('is_paused', models.BooleanField(default=False)),
                ('tokens', models.ManyToManyField(to='tokendb.Token')),
            ],
        ),
    ]
