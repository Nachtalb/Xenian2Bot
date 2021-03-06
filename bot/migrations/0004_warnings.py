# Generated by Django 2.2.4 on 2019-08-19 18:41

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_groupsettings_dev_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupsettings',
            name='groupname',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='Warnings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('count', models.IntegerField(default=0)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warnings', to='bot.GroupSettings')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warnings', to='bot.UserSettings')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
