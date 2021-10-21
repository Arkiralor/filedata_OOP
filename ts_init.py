import os
import datetime as dt


time_stamp = dt.datetime.now().timestamp()
time_stamp = str(time_stamp)

with open('last_access.txt', 'wt') as ts:
    ts.write(time_stamp)