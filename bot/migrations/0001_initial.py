# Generated by Django 2.2.4 on 2019-08-19 16:14

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('_user_state', models.CharField(choices=[('i', 'i'), ('d', 'd'), ('l', 'l'), ('e', 'e')], default='idle', max_length=100, verbose_name='State')),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('user_fullname', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
