#!/usr/bin/env python3.5

from conf import conf
from library.Classes import Classes
from models.Test import TestModel
from library.Middleware import rabbitmqWorkerFactory, Clear, TimeExpense
import time


class TestController(Classes.BaseMinix):
    default_method = 'get_all_user'  # 该属性为默认执行该类的业务处理方法

    def __init__(self):
        self.testModel = TestModel.getInstance()
        super().__init__()

    def prepare(self):
        print("先于执行业务方法执行的逻辑")

    @Clear
    def get_all_user(self):
        """
        Clear装饰器可手动控制资源的释放
        如不使用该装饰器则默认由框架自动管理
        """
        users = self.testModel.get_all_user()
        for user in users:
            print(user.nickname + '---' + user.loginname)

    def test_rabbitmq(self):
        @rabbitmqWorkerFactory(conf.rabbitmq.dsn, 'exchange_name', 'queue_name')
        def consum_mq(ch, method, properties, body):
            """ 在这里处理队列信息 """
            print(body)

    @TimeExpense
    def test_time_expense(self):
        """ 方法执行时间函数 """
        time.sleep(3)

    def test_params(self, one, two, three="hello"):
        print(one)
        print(two)
        print(three)
