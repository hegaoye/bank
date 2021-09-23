# coding=utf-8
import json


class Bill:
    """
    账单数据类
    """

    def __init__(self, serialNumber=None, transactionDate=None, transactionRemark=None, status=None, amount=None):
        self.serialNumber = serialNumber
        self.transactionDate = transactionDate
        self.transactionRemark = transactionRemark
        self.status = status
        self.amount = amount

    def to_json(self):
        return json.dumps(self.__dict__)
