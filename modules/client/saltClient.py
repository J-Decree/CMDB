from concurrent.futures import ThreadPoolExecutor
from . import BaseClient
from modules import plugins
from lib.log import PluginLogger
from lib.Json import Json
from conf import settings

class SaltClient(BaseClient):

    def __init__(self,*args,**kwargs):
        mode = settings.MODE
        if mode != 'salt':
            raise Exception('MODE must be agent in setting.py ')
        super(SaltClient,self).__init__(*args,**kwargs)


    def process(self):
        """
        根据主机名获取资产信息，将其发送到API
        :return:
        {
            "data": [ {"hostname": "c1.com"}, {"hostname": "c2.com"}],
           "error": null,
           "message": null,
           "status": true
        }
        """
        task = self.get_asset()
        logger = PluginLogger()
        if not task['status']:
            logger.log(task['message'], False)

        # 创建线程池：最大可用线程10
        pool = ThreadPoolExecutor(10)
        # "data": [ {"hostname": "c1.com"}, {"hostname": "c2.com"}],
        for item in task['data']:
            # c1.com  c2.com
            hostname = item['hostname']
            pool.submit(self.run, hostname)
            # run(c1.com) 1
            # run(c2.com) 2
        pool.shutdown(wait=True)

    def run(self, hostname):
        # 获取指定主机名的资产信息
        # {'status': True, 'message': None, 'error': None, 'data': {'disk': <lib.response.BaseResponse object at 0x00000000014686A0>, 'main_board': <lib.response.BaseResponse object at 0x00000000014689B0>, 'nic': <lib.response.BaseResponse object at 0x0000000001478278>, 'memory': <lib.response.BaseResponse object at 0x0000000001468F98>, 'os_platform': 'linux', 'os_version': 'CentOS release 6.6 (Final)', 'hostname': 'c1.com', 'cpu': <lib.response.BaseResponse object at 0x0000000001468E10>}}
        server_info = plugins.get_server_info(hostname)
        # 序列化成字符串
        server_json = Json.dumps(server_info.data)
        # 发送到API
        self.post_asset(server_json, self.callback)
