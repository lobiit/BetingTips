# Generated by Django 3.2.7 on 2021-10-05 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20211005_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.FloatField(max_length=20)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.group'),
        ),
    ]