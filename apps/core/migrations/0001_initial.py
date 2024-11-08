# Generated by Django 5.1.1 on 2024-10-09 03:03

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pitch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=20, prefix='PIT', unique=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(default='default/noimage.jpg', upload_to='images/pitches/')),
                ('image_1', models.ImageField(blank=True, upload_to='images/pitches/')),
                ('image_2', models.ImageField(blank=True, upload_to='images/pitches/')),
                ('location', models.CharField(max_length=255, verbose_name='Địa điểm')),
                ('price_per_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('size', models.CharField(choices=[('20mx40m', '20m x 40m'), ('30mx50m', '30m x 50m'), ('30mx60m', '30m x 60m'), ('68mx105m', '68m x 105m')], max_length=8, verbose_name='Kích thước')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=20, prefix='BOO', unique=True)),
                ('booking_date', models.DateField(verbose_name='Ngày đặt')),
                ('start_time', models.TimeField(verbose_name='Giờ bắt đầu')),
                ('end_time', models.TimeField(verbose_name='Giờ kết thúc')),
                ('messsage', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('booked', 'Đã đặt'), ('canceled', 'Đã hủy'), ('paid', 'Đã thanh toán')], default='booked', max_length=8)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pitch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pitch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=20, prefix='PAY', unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tổng tiền')),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name='Ngày thanh toán')),
                ('payment_method', models.CharField(choices=[('cash', 'Tiền mặt'), ('bank_transfer', 'Chuyển khoản'), ('credit_card', 'Thẻ tín dụng')], max_length=13, verbose_name='Phương thức thanh toán')),
                ('status', models.CharField(choices=[('pending', 'Chờ thành toán'), ('completed', 'Thanh toán thành công'), ('failed', 'Hủy thanh toán'), ('refunded', 'Hoàn tiền')], default='pending', max_length=9, verbose_name='Trạng thái')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.booking')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
