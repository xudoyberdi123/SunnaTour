# Generated by Django 4.1.5 on 2023-04-01 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sayt', '0012_paymeorder'),
        ('payme', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bron',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='sayt.tarifbron'),
            preserve_default=False,
        ),
    ]
