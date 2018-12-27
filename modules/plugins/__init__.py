from conf import settings
from modules.response import BaseResponse
import importlib


# PLUGINS_DICT = {
#     'cpu': 'modules.plugins.cpu.CpuPlugin',
#     'disk': 'modules.plugins.disk.DiskPlugin',
#     'main_board': 'modules.plugins.main_board.MainBoardPlugin',
#     'memory': 'modules.plugins.memory.MemoryPlugin',
#     'nic': 'modules.plugins.nic.NicPlugin',
# }
def get_server_info(hostname=None):
    """
      获取服务器基本信息
      :param hostname: agent模式时，hostname为空；salt或ssh模式时，hostname表示要连接的远程服务器
      :return:
      """
    response = BaseResponse()
    for k, v in settings.PLUGINS_DICT.items():
        module_path, cls_name = v.rsplit('.', 1)
        cls = getattr(importlib.import_module(module_path), cls_name)
        data = cls(hostname).execute()
        response.data[k] = data
    return response


if __name__ == '__main__':
    pass
