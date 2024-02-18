import calendar
import datetime


def get_calendar(offset: int = 0):
    now = datetime.datetime.now() + datetime.timedelta(days=offset * 29)
    cal = calendar.LocaleTextCalendar(locale='Russian_Russia').formatmonth(
        theyear=now.year,
        themonth=now.month,
        w=0, l=0)
    print(cal)
    # print(cal)
    # print([cal])
    cal = cal.split('\n')
    cal = [week.split(' ') for week in cal]
    complete_cal = list()
    for week in cal:
        complete_week = list()
        for day in week:
            if day != '':
                complete_week.append(day)
        complete_cal.append(complete_week)
    # print(complete_cal)

    keyboard = list()
    keyboard.append([
        [' '], [complete_cal[0][0]], [complete_cal[0][1]]
    ])

    for week in complete_cal[2:-1]:
        complete_week = list()
        print(week)
        if len(week) != 7:
            if week[0] == '1':
                for weekday in range(1, 8):
                    if weekday <= 7 - len(week):
                        complete_week.append(' ')
                    else:
                        complete_week.append(week[weekday - (7 - len(week) + 1)])
            else:
                for weekday in range(1, 8):
                    if weekday <= len(week):
                        complete_week.append(week[weekday - 1])
                    else:
                        complete_week.append(' ')
        else:
            [complete_week.append(day) for day in week]
        keyboard.append(complete_week)
    return keyboard


print(get_calendar(2))