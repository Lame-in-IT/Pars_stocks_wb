from datetime import datetime
from datetime import date, timedelta

def get_date_now():
    return "{:%Y-%m-%d}".format(datetime.now())        

def get_list_date_7():
    corrent_date = "{:%Y-%m-%d}".format(datetime.now())
    format_date = corrent_date.split("-")
    year = int(format_date[0])
    month = int(format_date[1])
    day = int(format_date[2])
    first_date = date(year, month, day)
    duration = timedelta(days=7)
    list_last_day = []
    for d in range(duration.days + 1):
        day = first_date - timedelta(days=d)
        list_last_day.append(day)
    return[list_last_day[0], list_last_day[1],
          list_last_day[2], list_last_day[3],
          list_last_day[4], list_last_day[5],
          list_last_day[6], list_last_day[7]]

def get_list_date_14():
    corrent_date = "{:%Y-%m-%d}".format(datetime.now())
    format_date = corrent_date.split("-")
    year = int(format_date[0])
    month = int(format_date[1])
    day = int(format_date[2])
    first_date = date(year, month, day)
    duration = timedelta(days=14)
    list_last_day = []
    for d in range(duration.days + 1):
        day = first_date - timedelta(days=d)
        list_last_day.append(day)
    return[list_last_day[0], list_last_day[1],
          list_last_day[2], list_last_day[3],
          list_last_day[4], list_last_day[5],
          list_last_day[6], list_last_day[7],
          list_last_day[8], list_last_day[9],
          list_last_day[10], list_last_day[11],
          list_last_day[12], list_last_day[13],
          list_last_day[14]
          ]

def get_date_7():
    corrent_date = "{:%Y-%m-%d}".format(datetime.now())
    format_date = corrent_date.split("-")
    year = int(format_date[0])
    month = int(format_date[1])
    day = int(format_date[2])
    first_date = date(year, month, day)
    duration = timedelta(days=7)
    list_last_day = []
    for d in range(duration.days + 1):
        day = first_date - timedelta(days=d)
        list_last_day.append(day)
    return list_last_day[7]

def gey_list_date_365():
    corrent_date_1 = "{:%Y, %m, %d}".format(datetime.now())
    format_date = corrent_date_1.split(",")
    year = int(format_date[0])
    month = int(format_date[1])
    day = int(format_date[2])
    first_date = date(year, month, day)
    duration_1 = timedelta(days=365)
    list_last_day_31 = []
    for d_1 in range(duration_1.days + 1):
        day_1 = first_date - timedelta(days=d_1)
        list_last_day_31.append(day_1)
    return list_last_day_31[365]

def gey_list_date_90():
    corrent_date_1 = "{:%Y, %m, %d}".format(datetime.now())
    format_date = corrent_date_1.split(",")
    year = int(format_date[0])
    month = int(format_date[1])
    day = int(format_date[2])
    first_date = date(year, month, day)
    duration_1 = timedelta(days=90)
    list_last_day_31 = []
    for d_1 in range(duration_1.days + 1):
        day_1 = first_date - timedelta(days=d_1)
        list_last_day_31.append(day_1)
    return list_last_day_31[90]

def gey_list_date_30():
    corrent_date_1 = "{:%Y, %m, %d}".format(datetime.now())
    format_date = corrent_date_1.split(",")
    year = int(format_date[0])
    month = int(format_date[1])
    day = int(format_date[2])
    first_date = date(year, month, day)
    duration_1 = timedelta(days=30)
    list_last_day_30 = []
    for d_1 in range(duration_1.days + 1):
        day_1 = first_date - timedelta(days=d_1)
        list_last_day_30.append(day_1)
    return[list_last_day_30[0], list_last_day_30[1],
          list_last_day_30[2], list_last_day_30[3],
          list_last_day_30[4], list_last_day_30[5],
          list_last_day_30[6], list_last_day_30[7],
          list_last_day_30[8], list_last_day_30[9],
          list_last_day_30[10], list_last_day_30[11],
          list_last_day_30[12], list_last_day_30[13],
          list_last_day_30[14], list_last_day_30[15],
          list_last_day_30[16], list_last_day_30[17],
          list_last_day_30[18], list_last_day_30[19],
          list_last_day_30[20], list_last_day_30[21],
          list_last_day_30[22], list_last_day_30[23],
          list_last_day_30[24], list_last_day_30[25],
          list_last_day_30[26], list_last_day_30[27],
          list_last_day_30[24], list_last_day_30[29],
          list_last_day_30[30],
    ]

def gey_list_date_60():
    corrent_date_1 = "{:%Y, %m, %d}".format(datetime.now())
    format_date = corrent_date_1.split(",")
    year = int(format_date[0])
    month = int(format_date[1])
    day = int(format_date[2])
    first_date = date(year, month, day)
    duration_1 = timedelta(days=60)
    list_last_day_30 = []
    for d_1 in range(duration_1.days + 1):
        day_1 = first_date - timedelta(days=d_1)
        list_last_day_30.append(day_1)
    return[list_last_day_30[0], list_last_day_30[1],
          list_last_day_30[2], list_last_day_30[3],
          list_last_day_30[4], list_last_day_30[5],
          list_last_day_30[6], list_last_day_30[7],
          list_last_day_30[8], list_last_day_30[9],
          list_last_day_30[10], list_last_day_30[11],
          list_last_day_30[12], list_last_day_30[13],
          list_last_day_30[14], list_last_day_30[15],
          list_last_day_30[16], list_last_day_30[17],
          list_last_day_30[18], list_last_day_30[19],
          list_last_day_30[20], list_last_day_30[21],
          list_last_day_30[22], list_last_day_30[23],
          list_last_day_30[24], list_last_day_30[25],
          list_last_day_30[26], list_last_day_30[27],
          list_last_day_30[24], list_last_day_30[29],
          list_last_day_30[30], list_last_day_30[31],
          list_last_day_30[32], list_last_day_30[33],
          list_last_day_30[34], list_last_day_30[35],
          list_last_day_30[36], list_last_day_30[37],
          list_last_day_30[38], list_last_day_30[39],
          list_last_day_30[40], list_last_day_30[41],
          list_last_day_30[42], list_last_day_30[43],
          list_last_day_30[44], list_last_day_30[45],
          list_last_day_30[46], list_last_day_30[47],
          list_last_day_30[48], list_last_day_30[49],
          list_last_day_30[50], list_last_day_30[51],
          list_last_day_30[52], list_last_day_30[53],
          list_last_day_30[53], list_last_day_30[55],
          list_last_day_30[56], list_last_day_30[57],
          list_last_day_30[58], list_last_day_30[59],
          list_last_day_30[60]
    ]

if __name__=="__main__":
    get_list_date_14()