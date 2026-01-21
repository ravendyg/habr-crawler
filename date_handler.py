'''
Parse habr dates, assume that all tim is in UTC.
'''

from dateutil.relativedelta import *
from dateutil import parser
from datetime import *

NOW = datetime.utcnow().replace(second=0, microsecond=0)
TODAY_START = NOW.replace(hour=0, minute=0)

def parse_date(date_str):
    '''
    Parse date.

    Args:
        date_str: habr date string

    Returns:
        date
    '''


    date, time = date_str.split('_')
    year, month, day = map(int, date.split('-'))
    hour, minute = map(int, time.split(':'))
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
