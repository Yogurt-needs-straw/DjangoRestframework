from django.db import models

class UserInfo(models.Model):
    """ 用户表 """

    role = models.IntegerField(verbose_name="角色", choices=((1, "总监"), (2, "经理"), (3, "员工")), default=3)

    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    # 临时方式、jwt
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True)

class Depart(models.Model):
    title = models.CharField(verbose_name="部门", max_length=32)
    order = models.IntegerField(verbose_name="顺序", )
    count = models.IntegerField(verbose_name="人数", )

class Tag(models.Model):
    caption = models.CharField(verbose_name="标签", max_length=32)

class UserInfo2(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")

    gender = models.SmallIntegerField(verbose_name="性别", choices=((1, "男"), (2, "女")))
    depart = models.ForeignKey(verbose_name="部门", to="Depart", on_delete=models.CASCADE)
    ctime = models.DateTimeField(verbose_name="时间", auto_now_add=True )

    tag = models.ManyToManyField(verbose_name="标签", to="Tag")


