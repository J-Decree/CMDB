from conf import settings
from .agentClient import AgentClient
from .saltClient import SaltClient
from .sshClient import SSHClient


def start_client():
    mode = settings.MODE
    if mode == 'agent':
        client = AgentClient()
    elif mode == 'salt':
        client = SaltClient()
    elif mode == 'ssh':
        client = SSHClient()
    else:
        raise Exception('setting MODE must be one of [ssh,salt,agent]')

    client.send()
