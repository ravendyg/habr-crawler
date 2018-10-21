#! /usr/bin/python3
# pylint: disable=C0103

"""
Download and parse lists of articles from habrahabr.ru and alike
"""

import os
import argparse
import json
import csv
from datetime import date
from pyquery import PyQuery as pq
from requests import get
import date_handler


def format_ending(input_str):
    '''
    Makes sure that there is a trailing "/"

    Args:
        input_str: some string

    Returns:
        output: the same string with "/" appended if there was none at the end
    '''
    if input_str[-1:] != '/':
        return input_str + '/'
    else:
        return input_str


parser = argparse.ArgumentParser(description='Process...')
parser.add_argument('--work_dir', type=str, help='destination directory')
parser.add_argument('--out_name', type=str, help='destination file')
parser.add_argument('--urls', type=str, help='sourse urls, comma separated')
parser.add_argument('--offset', type=int,
                    help='for how many days to load articles - optional',
                    default=7
                   )
args = parser.parse_args()

with open('config.json') as f:
    config = json.load(f)

if args.work_dir:
    work_dir = format_ending(args.work_dir)
else:
    work_dir = config['work_dir']

if args.out_name:
    out_name = args.out_name
else:
    out_name = date.today().strftime('habr-%m%d')


if not os.path.exists(work_dir):
    os.makedirs(work_dir)


stored_start_str = None
try:
    with open(work_dir + config['last_run_storage'], mode='r') as last_run_file:
        stored_start_str = last_run_file.readline()
except OSError:
    pass
stop = date_handler.get_stop(stored_start_str, args.offset)

good_authors = set()
try:
    with open(work_dir + config['good_authors'], mode='r') as good_file:
        content = good_file.readlines()
        for author in content:
            good_authors.add(author.strip())
except Exception:
    pass

bad_authors = set()
try:
    with open(work_dir + config['bad_authors'], mode='r') as bad_file:
        content = bad_file.readlines()
        for author in content:
            bad_authors.add(author.strip())
except Exception:
    pass

def get_articles(input_url):
    '''
    Get list of articles using the provided url

    Args:
        input_url: a url to be parsed

    Returns:
        articels: list of strings with article data (comma separated)
    '''
    page = get(input_url)
    dom = pq(page.text)
    links = dom('.post__title_link')

    page_urls = [link.attrib['href'] for link in links]
    dates = [date.text_content() for date in dom('.post__time')]
    authors = [auth.text_content() for auth in dom('.user-info__nickname')]
    titles = [link.text_content() for link in links]
    contents = [
        content.text_content().replace(',', '').replace('\r', ' ').replace('\n', ' ')
        for content in dom('.post__text')
        ]

    result = []

    for i in range(0, len(page_urls)):
        author = authors[i]
        if authors[i] in bad_authors:
            author = "'--- " + authors[i]
        elif authors[i] in good_authors:
            author = "@@@ " + authors[i]

        result.append({
            'id': int(page_urls[i].split('/')[-2]),  # a bit of hardcode
            'url': page_urls[i],
            'date': dates[i],
            'author': author,
            'title': titles[i],
            'content': contents[i]
        })

    return result


def serialize_article(article_dict):
    '''
    Serilize article dictionary

    Args:
        article_dict: an object

    Returns: string
    '''
    return ','.join([
        article_dict['url'],
        article_dict['date'],
        article_dict['author'],
        article_dict['title'],
        article_dict['content']
    ])

total_articles_loaded = 0

with open(work_dir + out_name, mode='a') as out_file:
    for raw_url in config['urls']:
        page_number = 1
        stop_time_reached = False

        while not stop_time_reached:
            url = '{}page{}'.format(raw_url, page_number)
            print(url)
            articles = get_articles(url)

            for article in articles:
                article_date = date_handler.parse_date(article['date'])
                if stop < article_date:
                    out_file.write('{}\n'.format(serialize_article(article)))
                    total_articles_loaded += 1
                else:
                    stop_time_reached = True
                    break
            page_number += 1

print('loaded {} at {}'.format(total_articles_loaded, date_handler.get_next_stop()))
with open(work_dir + config['last_run_storage'], mode='w') as last_run_file:
    print(date_handler.get_next_stop(), file=last_run_file)
