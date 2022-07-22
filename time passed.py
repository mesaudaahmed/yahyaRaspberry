import datetime

# class sheep:
#     pass
def savetime(firstTime):
    # firstTime = '16/03/22 16:15:19'
    first_time = datetime.datetime.strptime(firstTime, '%d/%m/%y %H:%M:%S')
    later_time = datetime.datetime.now()
    difference = later_time - first_time
    datetime.timedelta(0, 8, 562000)
    seconds_in_day = 24 * 60 * 60
    tup=divmod(difference.days * seconds_in_day + difference.seconds, 60)
    return int(tup[0]+tup[1]/60)
print(savetime('16/03/22 16:15:19'))
