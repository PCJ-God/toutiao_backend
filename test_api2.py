import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('101.35.89.37', username='root', password='@ilya050322', timeout=30)

# Test categories
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:8000/api/news/categories')
print('=== /api/news/categories ===')
print(stdout.read().decode()[:800])

# Test news list
cmd = "curl -s 'http://127.0.0.1:8000/api/news/list?categoryId=1&page=1&pageSize=2'"
stdin, stdout, stderr = ssh.exec_command(cmd)
print('\n=== /api/news/list ===')
print(stdout.read().decode()[:800])

ssh.close()