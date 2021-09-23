# coding=utf-8
import hashlib
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from dao.trade_record_dao import TradeRecordDao
from entity.bill import Bill
from service.basesv import BaseSV
from tools.browser import Browser
from tools.log4py import logger


class Bank(BaseSV):
    """
    银行驱动器
    """

    def __init__(self):
        super(Bank, self).__init__()
        self.driver = Browser().get_brower()

        # 详情页面 xpath
        self.detail_btn_id = 'ListTableWithCtrls.Rb1_mr.C2'
        self.detail_xpath = '//*[@id="VIEW_MINI_STATEMENT"]'

        # 返回上一级页面 xpath
        self.back_xpath = '//*[@id="BACK"]'
        self.back_parent_id = 'ListTableWithCtrls.Rb1_mr'
        self.tradeRecordDao = TradeRecordDao()

    def open_bank(self):
        """
        打开银行地址
        :return:
        """
        self.driver.get(self.bank)
        sleep(.5)

    def back(self):
        """
        向上一步操作
        :return:
        """
        sleep(1.5)
        back_parent = WebDriverWait(driver=self.driver, timeout=180, poll_frequency=0.5) \
            .until(EC.presence_of_element_located((By.ID, self.back_parent_id)))
        if back_parent:
            back = self.driver.find_element_by_xpath(self.back_xpath)
            if back:
                back.click()
                sleep(1)

    def go(self):
        """
        打开详情页
        :return:
        """
        sleep(1.5)
        go_btn = WebDriverWait(driver=self.driver, timeout=180, poll_frequency=0.5) \
            .until(EC.presence_of_element_located((By.ID, self.detail_btn_id)))
        if go_btn:
            go = self.driver.find_element_by_xpath(self.detail_xpath)
            if go:
                go.click()
                sleep(1)

    def bill_detail(self) -> list:
        """
        爬取数据
        :return: 数据集合
        """
        list = []

        txnHistoryList = WebDriverWait(driver=self.driver, timeout=180, poll_frequency=0.5) \
            .until(EC.presence_of_element_located((By.ID, 'transactionsList')))

        if txnHistoryList:
            listwhiterow = txnHistoryList.find_elements_by_class_name('listwhiterow')
            if listwhiterow:
                for row in listwhiterow:
                    data_list = row.find_elements_by_class_name('listgreyrowtxtleftline')
                    if data_list:
                        amount = data_list[4].text
                        amount = str(amount).replace(" ", "")
                        if amount.__len__() > 0:
                            bill = self.__get_bill(serialNumber=data_list[0].text, transactionDate=data_list[1].text,
                                                   transactionRemark=data_list[2].text, status='deposit',
                                                   amount=data_list[4].text)
                            if bill:
                                logger.info("发现新订单")
                                list.append(bill.__dict__)
                            else:
                                logger.info("订单重复")

            listgreyrow = txnHistoryList.find_elements_by_class_name('listgreyrow')
            if listgreyrow:
                for row in listgreyrow:
                    data_list = row.find_elements_by_class_name('listgreyrowtxtleftline')
                    if data_list:
                        amount = data_list[4].text
                        amount = str(amount).replace(" ", "")
                        if amount.__len__() > 0:
                            bill = self.__get_bill(serialNumber=data_list[0].text, transactionDate=data_list[1].text,
                                                   transactionRemark=data_list[2].text, status='deposit',
                                                   amount=data_list[4].text)
                            if bill:
                                logger.info("发现新订单")
                                list.append(bill.__dict__)
                            else:
                                logger.info("订单重复")

        return list

    def __get_bill(self, serialNumber=None, transactionDate=None, transactionRemark=None, status=None,
                   amount=None) -> Bill:
        '''
        检查订单信息是否重复
        :param serialNumber:
        :param transactionDate:
        :param transactionRemark:
        :param status:
        :param amount:
        :return:
        '''
        bill = Bill(serialNumber=serialNumber, transactionDate=transactionDate,
                    transactionRemark=transactionRemark, status=status, amount=amount)
        json = bill.to_json()
        logger.info(json)

        md5Hex = hashlib.md5(json.encode(encoding='utf-8')).hexdigest()
        record = self.tradeRecordDao.load(md5Hex)
        if not record:
            self.tradeRecordDao.insert(bill.serialNumber, md5Hex, bill.amount,
                                       bill.transactionRemark, bill.transactionDate)
            return bill
