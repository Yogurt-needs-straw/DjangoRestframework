# Generated by Django 3.2 on 2024-02-10 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drfdemo', '0002_userinfo_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Depart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='部门')),
                ('order', models.IntegerField(verbose_name='顺序')),
                ('count', models.IntegerField(verbose_name='人数')),
            ],
        ),
    ]
