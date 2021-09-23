# coding=utf-8
import json
from urllib import request

from tools.log4py import logger


def get(url):
    logger.debug("请求url: " + url)
    response = request.urlopen(url)
    result = response.read().decode(encoding='utf-8')
    if None != result:
        return result


def post(url, data=None) -> bool:
    try:
        logger.info("请求url: " + url)
        logger.info("请求参数: " + str(data))

        req = request.Request(url, data=json.dumps(data).encode('utf-8'), method="POST",
                              headers={'Content-Type': 'application/json'})
        response = request.urlopen(req)
        result = response.read().decode(encoding='utf-8')
        logger.info("请求响应-" + str(result))
        if result and str(result).__eq__('success'):
            logger.info("请求成功")
            return True
    except Exception as e:
        logger.error(e)
        return False
