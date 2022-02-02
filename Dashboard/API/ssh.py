import paramiko


def connect_ssh(ip: str, un: str, pw: str, filename: str):
    # Opent ssh connectie met aangegeven credentials
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,
                   username=un, password=pw, look_for_keys=False
                   )

    # Runt die file
    stdout = client.exec_command(f'python {filename}')[1]
    client.close()


def connect_ssh_lcd(ip: str, un: str, pw: str, filename: str, command):
    # Opent ssh connectie met aangegeven credentials
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,
                   username=un, password=pw, look_for_keys=False
                   )

    # Runt die file
    stdout = client.exec_command(f'python {filename} {command}')[1]
    client.close()
