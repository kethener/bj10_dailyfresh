# coding=utf-8
from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash
# Create your models here.


class PassportManager(models.Manager):
    '''
    用户模型管理器类
    '''
    def add_one_passport(self, username, password, email):
        '''
        添加一个用户账户信息
        '''
        # 获取self所在的模型类
        model_class = self.model
        # 创建一个模型类对象
        passport = model_class()
        passport.username = username
        passport.password = get_hash(password)
        passport.email = email
        # 保存进数据库
        passport.save()
        # 返回模型类对象
        return passport

    def get_one_passport(self, username, password=None):
        '''
        根据用户名密码查询账户信息
        '''
        try:
            if password is None:
                # 根据用户名查找账户信息
                passport = self.get(username=username)
            else:
                # 根据用户名和密码查询账户信息
                passport = self.get(username=username, password=get_hash(password)) #DoesNotExist #MultiObjectsReturn
        except self.model.DoesNotExist:
            passport = None
        return passport

# Passport.objects.add_one_passport()
# Passport.objects.get_one_passport()


class Passport(models.Model):
    '''
    用户账户模型类
    '''
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')

    objects = PassportManager() # 自定义模型管理器对象

    class Meta:
        db_table = 's_user_account' # 指定表名