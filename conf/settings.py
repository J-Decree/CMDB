import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODE = 'agent'  # ssh,salt

# 测试模式，仿造数据，用于测试函数是否成功运行,在单独的文件定义一个用于测试的继承BasePlugin类
TEXT_MODE = True

# 采集ssh方式，需要配置SSH的KEY和USER
SSH_PRIVATE_KEY_PATH = '/home/auto/.ssh/id_rsa'
SSH_USER = 'root'
SSH_PORT = 22

# 日志
# 错误日志的输出路径
ERROR_LOG_FILE = 'log/error.log'
# 正常运行日志输出路径
RUN_LOG_FILE = 'log/run.log'

# 各个插件的存放路径
PLUGINS_DICT = {
    'cpu': 'modules.plugins.cpu.CpuPlugin',
    'disk': 'modules.plugins.disk.DiskPlugin',
    'main_board': 'modules.plugins.main_board.MainBoardPlugin',
    'memory': 'modules.plugins.memory.MemoryPlugin',
    'nic': 'modules.plugins.nic.NicPlugin',
}

# client用于加密的key
SECRET_KEY = 'yiyidongwangbiqiyisheng13'
# 存放到request的header里,和认证数据（即加密的md5字符串配对）
AUTH_SIGN = 'auth-key' # 不能用下划线

# 远程服务器url，用于GET数据，场景是获取没有提交过数据的主机ip
REMOTE_URL = '127.0.0.1:8000'

#agent模式存储主机的文件路径
HOSTNAME_FILE_PATH = 'static/hostname'