from django.db import models

from db.base_manager import BaseManager
from db.base_models import BaseModel
from util.get_hash import get_hash

# Create your models here.


class PassportManager(BaseManager):
    """用户模型管理器类"""
    def add_one_passport(self, username, password, email):
        """添加一个用户信息"""
        # 先获取self所在的模型类
        model_class = self.model
        passport = model_class()
        passport.username = username
        passport.password = get_hash(password)
        passport.email = email
        # 保存到数据库
        passport.save()
        # 返回模型类对象
        return passport

    def get_one_passport1(self, username, password=None):
        """根据用户名和密码查询账户信息"""
        try:
            if password is None:
                # 根据用户名查找账户
                passport = self.get(username=username)
            else:
                # 根据用户名和密码查找账户
                passport = self.get(username=username, password=get_hash(password))
        except self.model.DoesNotExist:
                passport = None
        return passport

    def get_one_passport(self, username, password=None):
        '''
        根据用户名密码查询账户信息
        '''
        if password is None:
            # 根据用户名查找账户信息
            passport = self.get_one_object(username=username)
        else:
            # 根据用户名和密码查询账户信息
            passport = self.get_one_object(username=username, password=get_hash(password))
        return passport

# Passport.objects.add_one_passport()
# Passport.objects.get_one_passport()


class Passport(BaseModel):
    """用户账户模型类"""
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')

    # 自定义模型管理器对象
    objects = PassportManager()

    class Meta:
        # 自定义表名
        db_table = 's_user_account'


class AddressManager(BaseManager):
    """地址模型类管理器"""
    def get_default_address(self, passport_id):
        """获取账号的默认收货地址"""
        addr = self.get_one_object(passport_id=passport_id, is_def=True)
        return addr

    def add_one_address(self, passport_id, recipient_name,
                        recipient_addr, recipient_phone,
                        zip_code):
        """添加一个收货地址信息"""
        # 1.查询用户是否有默认收货地址
        def_addr = self.get_default_address(passport_id=passport_id)
        # 2. 判断
        if def_addr is None:
            # 用户没有默认收货地址
            addr = self.create_one_object(passport_id=passport_id, recipient_name=recipient_name,
                                          recipient_addr=recipient_addr, recipient_phone=recipient_phone,
                                          zip_code=zip_code, is_def=True)
        else:
            # 用户有默认收货地址
            addr = self.create_one_object(passport_id=passport_id, recipient_name=recipient_name,
                                          recipient_addr=recipient_addr, recipient_phone=recipient_phone,
                                          zip_code=zip_code)

        return addr


class Address(BaseModel):
    """地址模型类"""
    passport = models.ForeignKey('Passport', verbose_name='所属账户')
    recipient_name = models.CharField(max_length=20, verbose_name='收件人')
    recipient_addr = models.CharField(max_length=256, verbose_name='收件地址')
    recipient_phone = models.CharField(max_length=11, verbose_name='联系电话')
    zip_code = models.CharField(max_length=6, verbose_name='邮政编码')
    is_def = models.BooleanField(default=False, verbose_name='是否默认')

    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'
