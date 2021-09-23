# coding=utf-8

from tools.config import Config


class BaseSV:
    def __init__(self):
        """
        配置系统默认使用数据
        """
        self.config()

    def config(self):
        # 系统配置文件信息
        cfg = Config()
        # 读取频率
        self.time = cfg.read("sys", "time")
        # 银行
        self.bank = cfg.read("sys", "bank_url")
        # 推送数据接口
        self.push_api = cfg.read("sys", "push_data_url")
