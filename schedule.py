from pyquery import PyQuery as pq
from auth import authenticate
from datetime import datetime
from urllib import urlencode
from icalendar import Calendar, Event, UTC
import re
import json

def get_sio():

    s = authenticate('https://s3.as.cmu.edu/sio/index.html')
    s.headers['Content-Type'] = 'text/x-gwt-rpc; charset=UTF-8'

    siojs = s.get('https://s3.as.cmu.edu/sio/sio/sio.nocache.js').content
    permutation = re.search("Ub='([^']+)'", siojs).group(1)

    page_name = 'https://s3.as.cmu.edu/sio/sio/%s.cache.html' % (permutation)
    cachehtml = s.get(page_name).content

    # to successfully do RPC with SIO, you have to find the correct keys 
    # for each different kind of RPC you're doing and send them with the request
    def get_key(key):
        var_name = re.search("'%s',(\w+)," % key, cachehtml).group(1)
        return re.search("%s='([^']+)'" % var_name, cachehtml).group(1)

    context_key = get_key('userContext.rpc')
    content_key = get_key('bioinfo.rpc')
    
    schedule_data = {}

    # info in user context: full name, major/school
    s.post('https://s3.as.cmu.edu/sio/sio/userContext.rpc', 
           data=('7|0|4|https://s3.as.cmu.edu/sio/sio/|%s|edu.cmu.s3.ui.common.client.serverproxy.user.UserContextService|initUserContext|1|2|3|4|0|' % context_key))

    # get schedule
    cal = Calendar.from_string(s.get('https://s3.as.cmu.edu/sio/export/schedule/S14_semester.ics?semester=S14').content)
    day_map = {'MO': 'M', 'TU': 'T', 'WE': 'W', 'TH': 'R', 'FR': 'F'}
    schedule_data['schedule'] = []
    for event in cal.walk():
        if event.name != 'VEVENT': continue

        schedule_data['schedule'].append({
            'days': map(lambda day: day_map[day], event.get('rrule').get('byday')),
            'class_name': event.get('summary').strip(),
            'start_time': event.get('dtstart').dt,
            'end_time': event.get('dtend').dt
        })

    # parse JSON in format to be used by Django models
    # format eg: [{'class': '15210', 'times:' ['MWF:1200:1330', 'T:1330:1430']}]

    schedule_model_data = []
    schedule_data = schedule_data['schedule']

    # format separates lecture from recitation; first, get unique classes
    class_data = []
    for schedule_item in schedule_data:  
        class_name = schedule_item['class_name']
        class_name = str(class_name.split('::')[1].split(' ')[1])
        if (class_name not in class_data):
            class_data.append(class_name)

    # for every class, obtain days/times
    for class_item in class_data:
        class_obj = {}
        class_obj['class'] = class_item
        class_obj['time'] = []
        for schedule_item in schedule_data:
            if (class_item in schedule_item['class_name']):
                # extract time/dates and format, add to class_item object
                start_time = ''.join(str(schedule_item['start_time'].time()).split(':')[0:2])
                end_time = ''.join(str(schedule_item['end_time'].time()).split(':')[0:2])
                #concat strings together
                days = ''.join(schedule_item['days'])
                times = ':'.join([start_time, end_time])
                days_time = ''.join([days, times])
                class_obj['time'].append(days_time)
        print class_obj
        schedule_model_data.append(class_obj)

    #print "Done parsing"
    #print schedule_model_data



    return schedule_model_data


    {'schedule': [
                    {
                    'start_time': datetime.datetime(2014, 1, 14, 13, 30), 
                    'end_time': datetime.datetime(2014, 1, 14, 14, 50), 
                    'days': [2, 4], 
                    'summary': u'Foundations of Programming Languages :: 15312 1'}, 

                    {'start_time': datetime.datetime(2014, 1, 15, 11, 30), 
                    'end_time': datetime.datetime(2014, 1, 15, 12, 20), 'days': [3], 
                    'summary': u'Foundations of Programming Languages :: 15312 A'}, 


                    {'start_time': datetime.datetime(2014, 1, 13, 13, 30), 
                    'end_time': datetime.datetime(2014, 1, 13, 14, 50), 
                    'days': [1, 3], 
                    'summary': u'Parallel Computer Architecture and Programming :: 15418 A'}, 
                    {'start_time': datetime.datetime(2014, 1, 13, 10, 30), 
                    'end_time': datetime.datetime(2014, 1, 13, 11, 20), 
                    
                    'days': [1, 3, 5], 'summary': u'Physics II for Science Students :: 33112 1'}, 
                    {'start_time': datetime.datetime(2014, 1, 14, 12, 30), 
                    'end_time': datetime.datetime(2014, 1, 14, 13, 20), 
                    'days': [2, 4], 'summary': u'Physics II for Science Students :: 33112 D'}, 

                    {'start_time': datetime.datetime(2014, 1, 13, 9, 0), 
                    'end_time': datetime.datetime(2014, 1, 13, 10, 20), 
                    'days': [1, 3], 
                    'summary': u'Intermediate Microeconomics :: 73230 1'}, 
                    {'start_time': datetime.datetime(2014, 1, 17, 9, 0), 
                    'end_time': datetime.datetime(2014, 1, 17, 10, 20), 
                    'days': [5], 'summary': u'Intermediate Microeconomics :: 73230 B'}, 
                    
                    {'start_time': datetime.datetime(2014, 1, 13, 12, 30), 
                    'end_time': datetime.datetime(2014, 1, 13, 13, 20), 
                    'days': [1, 3], 'summary': u'Nature of Language :: 80180 1'}, 
                    {'start_time': datetime.datetime(2014, 1, 17, 11, 30), 
                    'end_time': datetime.datetime(2014, 1, 17, 12, 20), 
                    'days': [5], 'summary': u'Nature of Language :: 80180 B'}]}
