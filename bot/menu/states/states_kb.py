from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.bot_database import bot_db

import calendar
import datetime


async def get_places_kb(arg: str = 'search'):
    places = await bot_db.get_all_places()
    keyboard = [
        [InlineKeyboardButton(text=place[0], callback_data=f'{arg}-place|{place[0]}')] for place in places
    ]
    keyboard.append([InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-search')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_calendar_kb(arg: str, offset: int = 0):
    now = datetime.datetime.now() + datetime.timedelta(days=offset * 29)
    cal = calendar.LocaleTextCalendar(locale='Russian_Russia').formatmonth(
        theyear=now.year,
        themonth=now.month,
        w=0, l=0)
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

    month = complete_cal[0][0]
    year = complete_cal[0][1]
    keyboard = list()
    keyboard.append([
        InlineKeyboardButton(text='ㅤ', callback_data='none'),
        InlineKeyboardButton(text=month, callback_data=f'month-{arg}|{now.month.real}'),
        InlineKeyboardButton(text=year, callback_data=f'year-{arg}|{now.year.real}')
    ])

    for week in complete_cal[2:-1]:
        complete_week = list()
        if len(week) != 7:
            if week[0] == '1':
                for weekday in range(1, 8):
                    if weekday <= 7 - len(week):
                        complete_week.append(InlineKeyboardButton(text='ㅤ', callback_data='none'))
                    else:
                        complete_week.append(InlineKeyboardButton(text=week[weekday - (7 - len(week) + 1)],
                                                                  callback_data=(f'{arg}-day|' + week[
                                                                        weekday - (7 - len(week) + 1)] + now.strftime('.%m.%Y'))))
            else:
                for weekday in range(1, 8):
                    if weekday <= len(week):
                        complete_week.append(InlineKeyboardButton(text=week[weekday - 1],
                                                                  callback_data=(f'{arg}-day|' + week[
                                                                      weekday - 1] + now.strftime(
                                                                      '.%m.%Y'))))
                    else:
                        complete_week.append(InlineKeyboardButton(text='ㅤ', callback_data='none'))
        else:
            [complete_week.append(InlineKeyboardButton(text=day, callback_data=f'{arg}-day|' + day + now.strftime('.%m.%Y'))) for day in week]
        keyboard.append(complete_week)
    keyboard.append([
        InlineKeyboardButton(text='ㅤ', callback_data='none') if offset == 0 else
        InlineKeyboardButton(text='<-', callback_data=f'cal|{arg}|{offset - 1}'),
        InlineKeyboardButton(text='.', callback_data='dot'),
        InlineKeyboardButton(text='->', callback_data=f'cal|{arg}|{offset + 1}')
    ])
    keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='cancel-search')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_confirm_transfer_kb():
    keyboard = [
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm-trans'),
         InlineKeyboardButton(text='❌ Отменить', callback_data='cancel-trans')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)