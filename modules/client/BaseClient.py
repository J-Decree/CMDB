import hashlib
import time
import requests
import json
from conf import settings
from lib.log import PluginLogger


class BaseClient(object):

    def auth(self):
        # 认证方法，这个方法也是个
        secret_key = settings.SECRET_KEY
        auth_sign = settings.AUTH_SIGN
        t = time.time()
        m = hashlib.md5(secret_key.encode('utf8'))
        m.update(bytes("%s|%f" % (secret_key, t), encoding='utf8'))
        res = m.hexdigest()
        s = '%s|%f' % (res, t)
        return {auth_sign: s}

    def send(self):
        # 根据不同的mode方式，编写不同的发送代码
        raise NotImplementedError('you must implement send method')

    def get_uncommitted(self, callback=None):
        # 用于获得没有提交过数据的机子hostname集合，ssh模式和salt模式下使用

        """
        get方式向获取未采集的资产
        :return: {"data": [{"hostname": "c1.com"}, {"hostname": "c2.com"}], "error": null, "message": null, "status": true}
        """
        try:
            remote_url = settings.REMOTE_URL
            header = {}
            header.update(self.auth())
            data = requests.get(url=remote_url, header=header)
        except Exception as e:
            # 出错了，使用回调函数记录下来
            if callback:
                callback(status=False, msg=e)
            return
        return data.json()

    def post_data(self, data, callback=None):
        # 封装了requests.post请求发送数据，发送单一机子的数据。主要是减少重复代码
        try:
            remote_url = settings.REMOTE_URL
            header = {}
            header.update(self.auth())
            ret = requests.post(url=remote_url, header=header, data=data)
            status = True
        except Exception as e:
            # 出错了，使用回调函数记录下来
            ret = e
            status = False
        if callback:
            callback(status, ret)

        if status:
            return ret.json()

    def callback(self, status, data):
        """
               提交资产后的回调函数
               :param status: 是否请求成功
               :param response: 请求成功，则是响应内容对象；请求错误，则是异常对象
               :return:
               """
        logger = PluginLogger()
        if not status:
            logger.log(str(data), False)
            return

        # 请求成功，这个是requests.post返回的对象
        ret = json.loads(data.text)
        if ret['code'] == 1000:
            logger.log(ret['message'], True)
        else:
            logger.log(ret['message'], False)
