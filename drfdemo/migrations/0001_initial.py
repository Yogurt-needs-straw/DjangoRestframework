# Generated by Django 3.2 on 2024-02-20 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='标签')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, '总监'), (2, '经理'), (3, '员工')], default=3, verbose_name='角色')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('token', models.CharField(blank=True, max_length=64, null=True, verbose_name='TOKEN')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drfdemo.depart', verbose_name='部门')),
                ('tag', models.ManyToManyField(to='drfdemo.Tag', verbose_name='标签')),
            ],
        ),
    ]
