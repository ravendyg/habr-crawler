'''
Parse habr dates, assume that all tim is in UTC.
'''

from dateutil.relativedelta import *
from dateutil import parser
from datetime import *
import re

yesterday_regexp = r'вчера'
today_regexp = r'сегод'

NOW = datetime.utcnow().replace(second=0, microsecond=0)
TODAY_START = NOW.replace(hour=0, minute=0)

MONTH_DICT = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
}

def parse_date(date_str):
    '''
    Parse date.

    Args:
        date_str: habr date string

    Returns:
        date
    '''
    dt, tm = str.split(date_str.strip(), ' в ')[:2]
    hour, minute = str.split(tm.strip(), ':')

    if re.match(yesterday_regexp, dt):
        published = TODAY_START + relativedelta(days=-1)
    elif re.match(today_regexp, dt):
        published = TODAY_START
    else:
        day, month_str = str.split(dt.strip(), ' ')[:2]
        month = MONTH_DICT[month_str]
        published = TODAY_START.replace(month=month, day=int(day))

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
