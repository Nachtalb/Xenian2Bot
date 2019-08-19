# Generated by Django 2.2.4 on 2019-08-19 17:01

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupSettings',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('group_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('grouptitle', models.CharField(blank=True, max_length=200, null=True)),
                ('groupname', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
