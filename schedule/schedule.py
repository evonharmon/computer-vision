#!/usr/bin/env python
from __future__ import print_function
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime, timedelta
import re

# Parse command line arguments
try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument("field", help="Soccer field location")
    parser.add_argument("url", help="Team schedule website")
    flags = parser.parse_args()
except ImportError:
    flags = None

facility = flags.field
link = flags.url

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
denverId = 'p7h9gp4iqm0cl3cmv4t3g1k7oc@group.calendar.google.com'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def createEvent(date, start, cid):
    # Format date and time
    date = datetime.strptime(date, '%m-%d-%y').strftime('%Y-%m-%d')
    start = datetime.strptime(start, '%I:%M%p').strftime('%H:%M:%S')
    delta = timedelta(hours=1)
    end = datetime.strptime(start,'%H:%M:%S') + delta
    # Past midnight
    if end.hour == 0:
        end = end.replace(hour=23,minute=59)
    end = end.strftime('%H:%M:%S')
    # Combine
    sDateTime = date + "T" + start + "%s"
    eDateTime = date + "T" + end + "%s"

    # Add event to calendar
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    GMT_OFF = '-07:00'
    EVENT = {
        'summary': facility,
        'start':  {'dateTime': sDateTime % GMT_OFF},
        'end':    {'dateTime': eDateTime % GMT_OFF},
    }

    e = service.events().insert(calendarId=cid,
            sendNotifications=True, body=EVENT).execute()

    print('''*** %r event added:
        Start: %s
        End:   %s''' % (e['summary'].encode('utf-8'),
            e['start']['dateTime'], e['end']['dateTime']))


def main():
    # Open url
    html = urllib.urlopen(link).read()
    # Find dates and times
    dateFmt = " \\d{2}-\\d{2}-\\d{2} "
    timeFmt = " \\d{2}:\\d{2} "
    dates = re.findall(dateFmt, html)
    times = re.findall(timeFmt, html)

    # Set calendar id
    if facility == 'Denver':
        cid = denverId
    else:
        cid = 'primary'

    # Create event for each date
    for i in range(len(dates)):
        createEvent(dates[i].strip(),times[i].strip()+"PM",cid)


if __name__ == '__main__':
    main()
