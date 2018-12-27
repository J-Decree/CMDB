from conf import settings
from lib import log


# agent形式
# 1.采集资产
# 2.将资产数据发送到API（POST）

# SSH形式
# 1.获取今日未采集主机列表
# 2.采集资产
# 3.将资产数据发送到API（POST）

# Salt形式
# 1.获取今日未采集主机列表
# 2.采集资产
# 3.将资产数据发送到API（POST）

# 无论采用何种方法，都是使用cmd采集信息

class BasePlugin(object):
    def __init__(self, hostname=''):
        # 假设mode为agent,hostname为空
        self.hostname = hostname
        self.text_mode = settings.TEXT_MODE
        self.mode = settings.MODE
        self.logger = log.PluginLogger()
        mode_list = ['agent', 'ssh', 'salt']
        mode = settings.MODE
        if mode not in mode_list:
            raise Exception('采集方法MODE设置出错,必须是agent,ssh,salt')

    def agent(self, cmd):
        # 放在被监管的机子上运行
        import subprocess
        return subprocess.getoutput(cmd)

    def salt(self, cmd):
        # 脚本要在master机器上执行，执行用户需要是master用户
        import salt.client
        local = salt.client.LocalClient()
        res = local.cmd(self.hostname, 'cmd.run', [cmd])
        return res[self.hostname]

    def ssh(self, cmd):
        # 若使用此方法，则程序放在中转机上运行
        import paramiko
        private_key = paramiko.RSAKey.from_private_key_file(settings.SSH_PRIVATE_KEY_PATH)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname, port=settings.SSH_PORT, \
                    username=settings.SSH_USER, pkey=private_key)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        res = stderr.read()
        if not len(res): res = stdout.read()
        ssh.close()
        return res

    def exec_shell_cmd(self, cmd):
        func = getattr(self, self.mode)
        return func(cmd)

    def linux_collect(self):
        # 不同系统采集的信息不同，而非方法不同（因为有python这一层，无需考虑）
        # 但是不同的系统会导致采集的cmd命令不同。
        raise Exception('you must implement linux method')

    def windows_collect(self):
        raise Exception('you must implement windows method')

    def execute(self):
        return self.linux_collect()


if __name__ == '__main__':
    b = BasePlugin()
    # print(b.exec_shell_cmd())
