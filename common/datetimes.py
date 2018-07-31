# -*- coding:utf8 -*-
from time import strftime, localtime
from datetime import timedelta, date, datetime
import calendar

from common.base import tlock

year = strftime("%Y", localtime())
mon = strftime("%m", localtime())
day = strftime("%d", localtime())
hour = strftime("%H", localtime())
min = strftime("%M", localtime())
sec = strftime("%S", localtime())

def today():
    """返回当天的str类型YYYY-MM-DD"""
    return str(date.today())

def nowTime():
    """返回当前时间的str类型YYYY-MM-DD HH:MM:SS"""
    return strftime("%Y-%m-%d %H:%M:%S", localtime())

def addDays(days=0, mydate=None):
    """在当前的前提下加减天数，返回date类型YYYY-MM-DD"""
    if days < 0:
        if mydate:
            try:
                time = datetime.strptime(mydate, '%Y-%m-%d') - timedelta(days=days)
            except:
                from datetime import datetime as dt
                time = dt.strptime(mydate, '%Y-%m-%d') - timedelta(days=days)
            return time.strftime('%Y-%m-%d')
        else:
            return str(date.today() - timedelta(days=abs(days)))
    else:
        if mydate:
            try:
                time = datetime.strptime(mydate, '%Y-%m-%d') + timedelta(days=days)
            except:
                from datetime import datetime as dt
                time = dt.strptime(mydate, '%Y-%m-%d') + timedelta(days=days)
            return time.strftime('%Y-%m-%d')
        else:
            return str(date.today() + timedelta(days=days))

def addMonths(months=0, date=None):
    """在当前的前提下加减月数，返回date类型YYYY-MM-DD"""
    (y, m, d) = getyearandmonth(months) if not date else getyearandmonth(months,date)
    arr = (y, m, d)
    # if (int(day) < int(d)):
    #     arr = (y, m, day)
    return "-".join("%s" % i for i in arr)

def get_days_of_date(year, mon):
    """"返回指定月份的天数"""
    return calendar.monthrange(year, mon)[1]


def getyearandmonth(n=0,date=None):
    '''''
    get the year,month,days from today
    befor or after n months
    '''
    if date:
        time = date.split('-')
        thisyear,thismon = int(time[0]),int(time[1])
        totalmon = thismon+n
    else:
        thisyear, thismon = int(year),int(mon)
        totalmon = thismon + n
    if n >= 0:
        if totalmon <= 12:
            # days = str(get_days_of_date(thisyear, totalmon))
            totalmon = addzero(totalmon)
            dualDay = day if not date else time[2]
            days = dualDay
            if int(dualDay) == 31 and (totalmon in ('04', '06', '09', '11', 11)):
                days = 30
            if (int(dualDay) in (30, 31)) and (totalmon == '02'):
                if thisyear % 4 == 0 and thisyear % 100 != 0:
                    days = 29
                else:
                    days = 28
            days = addzero(days)
            return (year, totalmon, days) if not date else (time[0], totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if j == 0:
                i -= 1
                j = 12
            thisyear += i
            # days = str(get_days_of_date(thisyear, j))
            dualDay = day if not date else time[2]
            days = dualDay
            if int(dualDay) == 31 and (j in (4, 6, 9, 11)):
                days = 30
            if (int(dualDay) in (30, 31)) & j == 2:
                if thisyear % 4 == 0 and thisyear % 100 != 0:
                    days = 29
                else:
                    days = 28
            j = addzero(j)
            days = addzero(days)
            return str(thisyear), str(j), days
    else:
        if (totalmon > 0) and (totalmon < 12):
            # days = str(get_days_of_date(thisyear, totalmon))
            dualDay = day if not date else time[2]
            days = dualDay
            if int(dualDay) == 31 and (totalmon in ('04', '06', '09', '11', 11)):
                days = 30
            if (int(dualDay) in (30, 31)) and (totalmon == '02'):
                if thisyear % 4 == 0 and thisyear % 100 != 0:
                    days = 29
                else:
                    days = 28
            totalmon = addzero(totalmon)
            days = addzero(days)
            return (year, totalmon, days) if not date else (time[0],totalmon,days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if j == 0:
                i -= 1
                j = 12
            thisyear += i
            # days = str(get_days_of_date(thisyear, j))
            dualDay = day if not date else time[2]
            days = dualDay
            if int(dualDay) == 31 and (j in (4, 6, 9, 11)):
                days = 30
            if (int(dualDay) in (30, 31)) and j == 2 :
                if thisyear % 4 == 0 and thisyear % 100 != 0:
                    days = 29
                else:
                    days = 28
            j = addzero(j)
            days = addzero(days)
            return str(thisyear), str(j), days

def addzero(n):
    """
    add 0 before 0-9
    return 01-09
    """
    nabs = abs(int(n))
    if nabs < 10:
        return "0" + str(nabs)
    else:
        return nabs

def addMonthExDay(exDay, months=1, date=None):
    if date:
        time = date.split('-')
        thisyear, totalmon = int(time[0]), int(time[1])+months
    else:
        thisyear, totalmon = int(year),int(mon)+months
    if totalmon > 12:
        i = totalmon / 12
        j = totalmon % 12
        if j == 0:
            i -= 1
            j = 12
        thisyear += i
        totalmon = j
    if exDay == 30 and totalmon == 2:
        if thisyear % 4 == 0 and thisyear % 100 != 0:
            exDay = 29
        else:
            exDay = 28
    days = addzero(exDay)
    return "-".join("%s" % i for i in (str(thisyear), str(totalmon), days))

if __name__ == "__main__":
    a = addMonths(13, '2018-05-20')
    print a