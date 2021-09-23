# coding=utf-8
from time import sleep

from service.bank import Bank
from service.basesv import BaseSV
from tools.http import post
from tools.log4py import logger


class PaymentSV(BaseSV):
    """
    支付信息处理业务
    """

    def __init__(self):
        super(PaymentSV, self).__init__()
        self.bank = Bank()

    def run(self):
        """
        业务入口
        :return:
        """
        self.bank.open_bank()
        sleep(1)

        while True:
            # 进入到accouts页面
            self.bank.go()

            # 推送数据
            flag = self.__push()
            if flag:
                sleep(int(self.time))

                # 返回上级页面
                self.bank.back()
                sleep(int(self.time))

    def __push(self) -> bool:
        """
        推送数据到服务器
        :return:
        """
        data = self.bank.bill_detail()
        if data:
            post(self.push_api, data)
        else:
            logger.warn("无新订单")

        return True
