from datetime import timedelta , datetime
def daysPassed(firstTime):
    # firstTime = '16/03/22 16:15:19'
    first_time = datetime.strptime(firstTime, '%Y-%m-%d %H:%M:%S.%f')
    later_time = datetime.now()
    difference = later_time - first_time
    tup=divmod(difference.days,60)
    return tup[1]   
