# coding=utf-8
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

# pitop 配置文件
sys_conf = os.path.join(_basedir, 'sys.conf')

# cachedata 缓存文件
cache_json = os.path.join(_basedir, 'cache.json')

BROWSER_PATH=os.path.join(_basedir, 'chromedriver')

del os
