from concurrent.futures import ThreadPoolExecutor
from . import BaseClient
from modules import plugins
from lib.log import PluginLogger
from lib.Json import Json
from conf import settings


class SSHClient(BaseClient):
    def __init__(self, *args, **kwargs):
        mode = settings.MODE
        if mode != 'ssh':
            raise Exception('MODE must be agent in setting.py ')
        super(SSHClient, self).__init__(*args, **kwargs)

    def process(self):
        """
        根据主机名获取资产信息，将其发送到API
        :return:
        """
        task = self.get_uncommitted(callback=self.callback)
        logger = PluginLogger()
        if not task['status']:
            logger.log(task['message'], False)

        pool = ThreadPoolExecutor(10)
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run, hostname)
        pool.shutdown(wait=True)

    def run(self, hostname):
        server_info = plugins.get_server_info(hostname)
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json, self.callback)
