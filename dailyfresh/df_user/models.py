# coding=utf-8
from django.db import models
# 导入抽象模型基类
from db.base_model import BaseModel
# Create your models here.


class PassportManager(models.Manager):
    """定义用户模型管理器类"""
    def add_one_passport(self, username, password, email):
        # 获取self所在的模型类
        model_class = self.model
        # 创建一个模型类对象
        passport = model_class()
        # 获取用户信息
        passport.username = username
        passport.password = password
        passport.email = email
        # 保存用户信息到数据库
        passport.save()
        # 返回模型类对象
        return passport

    def get_one_passport(self, username, password=None):
        """根据用户名密码查询账户信息"""
        try:
            if password is None:
                passport = self.get(username = username)
            else:
                passport = self.get(username=username, password=password)
        except self.model.DoesNotExist:
            passport = None

        return passport


class Passport(models.Model):
    """用户账户模型类"""
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')

    objects = PassportManager()

    class Meta:
        # 指定表名
        db_table = 's_user_account'
