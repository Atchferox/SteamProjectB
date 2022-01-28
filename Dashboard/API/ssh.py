import paramiko


def send_file(ip: str, un: str, pw: str, file: str):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,
                   username=un, password=pw, look_for_keys=False
                   )

    sftp = client.open_sftp()
    sftp.put(__file__, file)
    sftp.close()

    stdout = client.exec_command(f'python {file}')[1]
    for line in stdout:
        print(line)

    client.close()
