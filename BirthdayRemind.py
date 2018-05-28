#coding:utf-8

import tools.LunarSolarConverter as LSC
import tools.mailService as ms
import pandas as pd
from datetime import datetime

now = datetime.now()

#该函数用以返回今年生日阳历日期，如果生日已经过了，则返回明年生日日期
def CurrentSolarDays(url):

    converter = LSC.LunarSolarConverter()

    now_year = datetime.today().year
    now_month = datetime.today().month
    now_day = datetime.today().day
    # 今天的阳历年
    now_solar = LSC.Solar(now_year, now_month, now_day)
    # 计算今天所属哪个阴历年(比如2019年1月1日其实阴历年是2018年)
    now_lunar_year = converter.SolarToLunar(now_solar)[1]

    #读取数据
    data = pd.read_excel(url)
    df = data.values

    currentsolarydays = {}
    for i in df:
        name = i[1]
        birthday = str(i[2])
        birthday_year = int(birthday[:4])
        birthday_month = int(birthday[4:6])
        birthday_day = int(birthday[-2:])
        #生日是按照阴历还是阳历进行计算的
        lunar = i[3]

        if lunar:
            #计算今年的阴历生日，并转换为阳历
            lunar = LSC.Lunar(now_lunar_year,birthday_month,birthday_day,isleap = LSC.is_leap_year(now_lunar_year))
            now_solar_year,now_solar_month,now_solar_day = converter.LunarToSolar(lunar)
            now_solar_bithday = str(now_solar_year)+str(now_solar_month)+str(now_solar_day)
            #如果生日已经过了，则计算下一年生日
            if (now - datetime.strptime(now_solar_bithday,'%Y%m%d')).days > 0:
                lunar = LSC.Lunar(now_lunar_year + 1, birthday_month, birthday_day, isleap = LSC.is_leap_year(now_lunar_year+1))
                now_solar_year, now_solar_month, now_solar_day = converter.LunarToSolar(lunar)
                now_solar_bithday = str(now_solar_year) + str(now_solar_month) + str(now_solar_day)
            currentsolarydays[str(name)] = datetime.strptime(now_solar_bithday,'%Y%m%d')
        else:
            now_solar_bithday = str(now_year) + str(birthday_month) + str(birthday_day)
			#如果生日已过，则计算下一年阳历生日
            if (now - datetime.strptime(now_solar_bithday,'%Y%m%d')).days > 0:
                now_solar_bithday = str(now_year+1) + str(birthday_month) + str(birthday_day)
            currentsolarydays[str(name)] = datetime.strptime(now_solar_bithday,'%Y%m%d')
			
    return currentsolarydays

	
#使用邮件提醒,默认小于7天开始提醒；
def BirthdayRemin(currentsolarydays,remindnum = 7):
    content = {}
    for name,birthday in currentsolarydays.items():
        delta = (birthday - now).days + 1
        if delta <= remindnum:
            content[str(name)] = delta
    return sorted(content.items(),key = lambda x:x[1])


if __name__ == '__main__':
    #如果使用windows计划任务，建议生日路径写绝对路径，因为相对路径会报错。。
    data_url = 'data/BirthdayRemind.xlsx'
    from_addr = to_addr = 'your email address'
    password = 'your password'
	#附件路径
    filepath = []
	
	#邮件正文
    content = '生日提醒:' + '\n'
    birthday_data = BirthdayRemin(currentsolarydays=CurrentSolarDays(data_url))
    if birthday_data:
        for i in birthday_data:
            name = i[0]
            days = i[1]
            content = content + '距离 %s 生日还有 %s 天，快来准备礼物吧~' % (name,days) + '\n'
        ms.mail_send_service(from_addr=from_addr,password=password,to_addr=to_addr,content=content,filepath=filepath)
    else:
        print('还没到好友生日哦~')
