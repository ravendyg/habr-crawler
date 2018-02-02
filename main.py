#! /usr/bin/python3
# pylint: disable=C0103

"""
Download and parse lists of articles from habrahabr.ru and alike
"""

import os
import argparse
import json
import csv
from pyquery import PyQuery as pq
from requests import get


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
parser.add_argument('--count', type=int,
                    help='how many articles to load - optional',
                    default=-1
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
    out_name = config['out_name']

if args.count > 500:
    count = 500
else:
    count = args.count

if not os.path.exists(work_dir):
    os.makedirs(work_dir)


stop_id_dict = {}
next_stop_id_dict = {}
try:
    with open(work_dir + config['stop_id_storage'], mode='r') as id_dict_file:
        for key, val in csv.reader(id_dict_file):
            stop_id_dict[key] = int(val)
except OSError:
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
        result.append({
            'id': int(page_urls[i].split('/')[-2]),  # a bit of hardcode
            'url': page_urls[i],
            'date': dates[i],
            'author': authors[i],
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


with open(work_dir + out_name, mode='a') as out_file:
    for raw_url in config['urls']:
        page_number = 1
        articles_left = count
        stop_id = stop_id_dict.get(raw_url, 0)

        limit_reached = False or articles_left == 0
        while not limit_reached:
            url = '{}page{}'.format(raw_url, page_number)
            print(url)
            articles = get_articles(url)
            if page_number == 1:
                next_stop_id_dict[raw_url] = articles[0]['id']
            for article in articles:
                limit_reached = article['id'] == stop_id or articles_left == 0
                if not limit_reached:
                    articles_left -= 1
                    out_file.write('{}\n'.format(serialize_article(article)))
                else:
                    break
            page_number += 1

print(next_stop_id_dict)
with open(work_dir + config['stop_id_storage'], mode='w') as id_dict_file:
    writer = csv.writer(id_dict_file, delimiter=',')
    for key, value in next_stop_id_dict.items():
        writer.writerow([key, value])
