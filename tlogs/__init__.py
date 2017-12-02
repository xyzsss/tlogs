from .tlogs import app
import datetime


# def clever_function():
#     return u'HELLO'


def getype(a):
    # return a
    date_val = datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S.%f")
    # print(type(date_val))
    (day, hour, minute, second) = get_date_passed(date_val)
    if day > 0:
        delay_string = "%s d %s h %s m %s s" % (day, hour, minute, second)
    elif hour > 0:
        delay_string = "%s h %s m %s s" % (hour, minute, second)
    elif minute > 0:
        delay_string = "%s m %s s" % (minute, second)    
    else:
        delay_string = "%s s" % (second)
    return delay_string + " ago"


def get_date_passed(time_value):
    now = datetime.datetime.now()
    seconds = (now - time_value).total_seconds()
    day = int(seconds / 86400)
    hour = int((seconds - day * 86400) / 3600)
    minute = int((seconds - day * 86400 - hour * 3600) / 60)
    second = int(seconds - day * 86400 - hour * 3600 - minute * 60)
    return (day, hour, minute, second)


app.jinja_env.globals.update(getype=getype)
