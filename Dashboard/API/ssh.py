import paramiko


def send_file(ip: str, un: str, pw: str, localfile: str, remotefile: str, filename: str):
    # Opent ssh connectie met aangegeven credentials
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,
                   username=un, password=pw, look_for_keys=False
                   )

    # Upload de file naar de pi
    sftp = client.open_sftp()
    sftp.put(localfile, remotefile)
    sftp.close()

    # Runt die file
    stdout = client.exec_command(f'python {filename}')[1]
    for line in stdout:
        # Voor testen
        print(line)

    client.close()
