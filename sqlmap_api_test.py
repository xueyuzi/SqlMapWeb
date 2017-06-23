#!/usr/bin/python
#-*-coding:utf-8-*-
import requests
import time
import json
import sqlite3

class AutoSqli(object):

    def __init__(self, server='', target='', data='', referer='', cookie=''):
        super(AutoSqli, self).__init__()
        self.server = server
        if self.server[-1] != '/':
            self.server = self.server + '/'
            self.target = target
            self.taskid = ''
            self.engineid = ''
            self.status = ''
            self.data = data
            self.referer = referer
            self.cookie = cookie
            self.start_time = time.time()

# 新建扫描任务


    def task_new(self):
        self.taskid = json.loads(
            requests.get(self.server + 'task/new').text)['taskid']
        print('Created new task: ' + self.taskid)
        # 得到taskid,根据这个taskid来进行其他的
        if len(self.taskid) > 0:
            return True

    # 删除扫描任务


    def task_delete(self):
        if json.loads(requests.get(self.server + 'task/' + self.taskid + '/delete').text)['success']:
            print('[%s] Deleted task' % (self.taskid))
            return True


    # 扫描任务开始


    def scan_start(self):
        headers = {'Content-Type': 'application/json'}
        # 需要扫描的地址
        payload = {'url': self.target, 'cookie': self.cookie,}
        url = self.server + 'scan/' + self.taskid + '/start'
        # http://127.0.0.1:8557/scan/xxxxxxxxxx/start
        t = json.loads(
            requests.post(url, data=json.dumps(payload), headers=headers).text)
        self.engineid = t['engineid']
        if len(str(self.engineid)) > 0 and t['success']:
            print('Started scan')
            return True

    # 扫描任务的状态


    def scan_status(self):
        self.status = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/status').text)['status']
        return self.status

    # 扫描任务的细节


    def scan_data(self):
        self.data = json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/data').text)['data']
        if len(self.data) == 0:
            print('not injection:\t')
        else:
            print('injection:\t' + self.target)

    # 扫描的设置,主要的是参数的设置


    def option_set(self):
        headers = {'Content-Type': 'application/json'}
        option = {
                    "smart": True,
                    "getDbs": True,
                    "textOnly": True,
                    "titles": True,
                }
        print(option)
        url = self.server + 'option/' + self.taskid + '/set'
        t = json.loads(
            requests.post(url, data=json.dumps(option), headers=headers).text)
        # print(t)

    # 停止扫描任务


    def scan_stop(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/stop').text)['success']

    # 杀死扫描任务进程


    def scan_kill(self):
        json.loads(
            requests.get(self.server + 'scan/' + self.taskid + '/kill').text)['success']

    def get_report(self):
        return requests.get(self.server + 'scan/' + self.taskid + '/data').json()

    def run(self):
        if not self.task_new():
            return False
            self.option_set()
        if not self.scan_start():
            return False


# if __name__ == '__main__':

#     DATABASE = './database.db'
#     conn = sqlite3.connect(DATABASE)
#     SqlMapServer = 'http://192.168.1.113:8775'
#     target = 'http://192.168.1.77/DVWA-master/vulnerabilities/sqli/?id=1&Submit=Submit&user_token=fb3db138005384dfbff27dd3c9e17f10'
#     cookie = 'security=low; PHPSESSID=5a8e2f5h6050924ubqsm3dcsq6'
#     tasks = AutoSqli(SqlMapServer, target, cookie=cookie)
#     # 创建task
#     tasks.task_new()
#     # 开始扫描
#     # tasks.scan_start()
#     # # 轮询扫描结果
#     tasks.option_set()
#     status = tasks.scan_status()

#     # 结束后获取结果
#     # tasks.taskid='531c0320be6820e5'
#     print(tasks.get_report())
