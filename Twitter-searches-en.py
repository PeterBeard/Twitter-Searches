#!/usr/bin/python3
# Search Twitter using Tweepy
# This program uses the module Tweepy to search Twitter for tweets with the two given tags.

import tweepy
import time
import csv, openpyxl
import configparser
import argparse
import re
from io import StringIO
from datetime import date, timedelta

# Some constants
CONFIG_FILE = 'config.ini'      # Location of config file
DATE_FORMAT = '%Y-%m-%d'        # Format string for dates

# Parse a time string to an integer number of seconds
def time_in_secs(time_str):
    time_str = time_str.strip().lower()
    matches = re.match('(\d+)\s*(\w+)s?', time_str)
    # Raise an exception on invalid input
    if not matches:
        raise ValueError('Invalid time string')

    # Handle valid input
    value = matches.group(1)
    unit = matches.group(2)
    if unit == 'day' or unit == 'd':
        return 86400 * int(value)
    elif unit == 'hour' or unit == 'h':
        return 3600 * int(value)
    elif unit == 'minute' or unit == 'min' or unit == 'm':
        return 60 * int(value)
    elif unit == 'second' or unit == 'sec' or unit == 's':
        return int(value)
    # Raise an exception for unknown units
    raise ValueError('Unknown time units')

# Read config file
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

username = config['common']['username']
password = config['common']['password']
consumer_token = config['common']['consumer_token']
consumer_secret = config['common']['consumer_secret']

access_token = config['common']['access_token']
access_secret = config['common']['access_secret']

default_format = config['common']['default_format']
default_lang = config['common']['default_lang']

# Get command line arguments
parser = argparse.ArgumentParser(description='')
parser.add_argument('-l','--lang', default=default_lang, help='The desired language of returned tweets (ISO 639-1)')
parser.add_argument('-f','--format', default=default_format, help='The output format. Options are csv or xls.')
parser.add_argument('-o','--outfile', help='The name of the output file. Output will be on STDOUT if not specified.')
parser.add_argument('-t','--time', default='1 day', help='The distance in the past to search. Understands days, hours, minutes, seconds (d, h, m, s).')
parser.add_argument('-n','--number', default=0, help='The number of tweets to return. Default is no limit.', type=int)
parser.add_argument('term',help='The term(s) to search for')

args = parser.parse_args()

search_term = args.term
lang = args.lang.lower()
time_window = time_in_secs(args.time)
outfile = args.outfile
output_format = args.format.lower()
n_tweets = args.number

# Make sure language matches ISO 639-1 (i.e. two characters long)
if len(lang) != 2:
    # Fall back to default
    lang = default_lang

# Create file handler if we're writing to a file
if outfile:
    if output_format == 'xls' or output_format == 'xlsx':
        output_handle = open(outfile, 'wb')
    else:
        output_handle = open(outfile, 'w')
# Otherwise use a string (to be printed to STDOUT)
else:
    if not (output_format == 'xls' or output_format == 'xlsx'):
        output_handle = StringIO()
    # XLS is a binary format and can't be printed to STDOUT
    else:
        raise ValueError('XLS and XLSX must be written to a file using -o')

# Use the right kind of output handler
if output_format == 'csv':
    csvWriter = csv.writer(output_handle)
elif output_format == 'xls' or output_format == 'xlsx':
    wb = openpyxl.Workbook()
    ws = wb.active
    
else:
    raise ValueError('Unknown output format')

#search parameters
today = date.today()
startSince = today - timedelta(seconds=time_window)
# If the limit isn't in the future then Twitter won't show things from today
endUntil = today + timedelta(days=1)

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
mysearch = tweepy.Cursor(api.search,q=search_term, since=startSince, until=endUntil, lang=lang).items()

count = 0
while count < n_tweets or n_tweets <= 0:
    try:
        tweet = mysearch.next()
        if output_format == 'csv':
            csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
        elif output_format == 'xls' or output_format == 'xlsx':
            ws.append([tweet.created_at, tweet.text.encode('utf-8')])
        count += 1
    except tweepy.TweepError:
        time.sleep(60 * 15)
        continue
    except:
        break

# Save the XLS file
if output_format == 'xls' or output_format == 'xlsx':
    wb.save(output_handle)

# Print to STDOUT
if not outfile:
    print(output_handle.getvalue())

# Close the file handle
output_handle.close()
