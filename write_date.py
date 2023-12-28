from dir_info import *
import sys
import datetime as dt

if len(sys.argv) > 1:
    today = str(sys.argv[1])
else:   # no date is provided
    today = dt.datetime.today().strftime('%Y-%m-%d')

year, month, day = today.split('-')
date = dt.datetime(int(year), int(month), int(day), 00, 00, 00)
# print(date.weekday())
while date.weekday() >= 5:  # if today is weekend, use Friday
    date -= dt.timedelta(1)

today = date.strftime('%Y-%m-%d')
    
with open(codedir + 'date_info.py', 'w') as f:
    f.write('today = \'' + today + '\'')
