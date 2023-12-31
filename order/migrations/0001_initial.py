# Generated by Django 4.1.2 on 2022-10-17 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('transaction_type', models.PositiveSmallIntegerField()),
                ('status', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(editable=False)),
                ('modified_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]
