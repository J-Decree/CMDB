import os
import json
from . import BaseClient
from conf import settings
from modules import plugins


class AgentClient(BaseClient):
    def __init__(self, *args, **kwargs):
        mode = settings.MODE
        if mode != 'agent':
            raise Exception('MODE must be agent in setting.py ')
        super(AgentClient, self).__init__(*args, **kwargs)

    def store_hostname(self, hostname):
        path = settings.HOSTNAME_FILE_PATH
        if not os.path.exists(path):
            os.makedirs(os.path.basename(path))

        with open(path, 'w') as f:
            f.write(hostname)

    def get_hostname_by_file(self):
        path = settings.HOSTNAME_FILE_PATH
        if not os.path.exists(path):
            return

        with open(path, 'r') as f:
            data = f.read()

        if not data:
            return

        return data.strip()

    def send(self):
        """
       获取当前资产信息
       1. 在资产中获取主机名 cert_new
       2. 在本地cert文件中获取主机名 cert_old
       如果cert文件中为空，表示是新资产
           - 则将 cert_new 写入该文件中，发送数据到服务器（新资产）
       如果两个名称不相等
           - 如果 db=new 则，表示应该主动修改，new为唯一ID
           - 如果 db=old 则，表示意外修改
       :return:
       """
        send_info = plugins.get_server_info()
        if not send_info.status:
            return

        cert_old = self.get_hostname_by_file()
        cert_new = send_info.data['hostname']
        if not cert_old:
            self.store_hostname(cert_new)
        else:
            if cert_old != cert_new:
                send_info.data['hostname'] = cert_old

        self.post_data(json.dumps(send_info.data), self.callback)
