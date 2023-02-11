'''
Parse habr dates, assume that all tim is in UTC.
'''

from dateutil.relativedelta import *
from dateutil import parser
from datetime import *
import re

yesterday_regexp = r'.*вчера'
today_regexp = r'.*сегод'
fancy_today_regexp = r'.*назад'

NOW = datetime.utcnow().replace(second=0, microsecond=0)
TODAY_START = NOW.replace(hour=0, minute=0)

MONTH_DICT = {
    'янв': 1,
    'фев': 2,
    'мар': 3,
    'апр': 4,
    'мая': 5,
    'июн': 6,
    'июл': 7,
    'авг': 8,
    'сен': 9,
    'окт': 10,
    'ноя': 11,
    'дек': 12,
}

def parse_date(date_str):
    '''
    Parse date.

    Args:
        date_str: habr date string

    Returns:
        date
    '''
    if re.match(fancy_today_regexp, date_str) or date_str == '':
        return TODAY_START

    dt, tm = re.split(r' в ', date_str.strip())
    hour, minute = str.split(tm.strip(), ':')

    if re.match(yesterday_regexp, dt):
        published = TODAY_START + relativedelta(days=-1)
    elif re.match(today_regexp, dt):
        published = TODAY_START
    else:
        day, _, month_str = str.split(dt.strip(), ' ')[:3]
        month = MONTH_DICT[month_str]
        n = datetime.now()
        year = n.year
        #  There is no year in the date anymore. For the last December set previous year.
        if month == 12 and n.month == 1:
            year -= 1
        published = TODAY_START.replace(year=year, month=month, day=int(day))

    return published.replace(hour=int(hour), minute=int(minute))

def get_stop(date_str=None, offset=7):
    '''
    Calculate stop date.
    Either parse previously stored or day start <offset> days before.

    Args:
        date_str: string - date
        offset: number - days to be subtracted from today

    Returns:
        date
    '''
    if date_str is not None:
        return parser.parse(date_str)
    else:
        now = TODAY_START
        return now + relativedelta(days=-offset)

def get_next_stop():
    '''Calculate the next stop time

    Returns:
        date
    '''
    return NOW
