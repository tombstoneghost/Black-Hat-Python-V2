# Imports
import paramiko
import getpass


def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()

    if output:
        print('*'*5 + "Output" + "*"*5)

        for line in output:
            print(line.strip())


if __name__ == "__main__":
    user = input('Username: ')
    passwd = getpass.getpass()

    ip = input('Enter Server IP: ')
    port = input('Enter Port: ')
    cmd = input('Enter Command: ')


    ssh_command(ip=ip, port=port, user=user, passwd=passwd, cmd=cmd)
