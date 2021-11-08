import datetime

datetime_now = datetime.datetime.now()
date_1 = datetime_now.strftime('%H:%M - %d.%m.%Y')
print(datetime_now)
print(date_1)