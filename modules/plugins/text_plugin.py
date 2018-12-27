from .base_plugin import BasePlugin
from modules.response import BaseResponse
import traceback


class TextPlugin(BasePlugin):
    def linux_collect(self):
        response = BaseResponse()
        try:
            ret = {
                'os_platform': self.collect_platform(),
                'os_version': self.collect_version(),
                'os_hostname': self.collect_hostname(),
            }
            response.data = ret
        except Exception as e:
            msg = "%s BasicPlugin Error:%s"
            self.logger.log(msg % (self.hostname, traceback.format_exc()), False)
            response.status = False
            response.error = msg % (self.hostname, traceback.format_exc())

        return response

    def collect_hostname(self):
        if self.text_mode:
            return 'Linux'
        else:
            res = self.exec_shell_cmd('uname')
            return res.strip()

    def collect_version(self):
        if self.text_mode:
            return 'Darwin-17.2.0-x86_64-i386-64bit'
        else:
            res = self.exec_shell_cmd('cat /etc/issue')
            return res.strip()

    def collect_platform(self):
        if self.text_mode:
            return 'c1.com'
        else:
            res = self.exec_shell_cmd('hostname')
            return res.strip()
