#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import time
import re

import requests

"""
如果获取不到请检查cookie和bkn是否与浏览器请求cookie和bkn一致,是否已加入目标群号.
"""

def get_qq_group_people(cookie, group_number, bkn):
	header = {
	'Cookie': cookie,
	"origin": "https://qun.qq.com",
	"referer": "https://qun.qq.com/member.html",
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
	}
	post_data = {
    'gc': group_number, # 目标群号
    'st': '0', # 从第几名用户开始
    'end': '5000', # 从第几名用户结束
    'sort': '0', # 目测正序反序，木研究
    'bkn': bkn, # bkn算法 http://s.url.cn/qqfind/js/find.2ce78a60.js
	}
	response = requests.post("https://qun.qq.com/cgi-bin/qun_mgr/search_group_members", headers=header, data=post_data)
	response.encoding = 'utf-8'
	return response.json()

cookie = input("[*] Please input you cookie: ") # F12获取请求的cookie
group_number = input("[+] Please input target group number: ") # 目标群号
bkn = input("[+] Please input bkn params: ") # F12获取请求的bkn

with open(group_number+".txt", 'a', encoding='utf-8') as f:
	response = get_qq_group_people(cookie, group_number, bkn)
	mems = response['mems']
	for content in mems:
		if content['g'] == 0:
			gander =  '男'
		elif content['g'] == 1:
			gander =  '女'
		elif content['g'] == 255:
			gander = '未知'
		data = {
			'昵称：': content['nick'].replace('&nbsp',' '),
			'群名片：': content['card'],
			'QQ：': str(content['uin']),
			'性别：': gander,
			'Q龄：': str(content['qage'])+'年',
			'入群时间：': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(content['join_time'])),
			'群聊等级：': response['levelname'][str(content['lv']['level'])]+'('+str(content['lv']['point'])+')',
			'最后发言：': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(content['last_speak_time'])),
		}
		print(data)
		f.write(str(data)+'\n')
		with open(group_number+'_QQ.txt', 'a') as ff:
			ff.write(data['QQ：']+'\n')
