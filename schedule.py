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
        schedule_model_data.append(class_obj)

    self_stime = "T1500"
    self_etime = "T1800"
    print "self_stime: " + self_stime[1:] + " self_etime: " + self_etime[1:]
    free = True
    self_day = self_stime[0] # assuming stime/etime have same days
    self_stime = int(self_stime[1:])
    self_etime = int(self_etime[1:])
    # iterate through all classes
    for class_item in schedule_model_data: 
      class_time = class_item['time']
      # iterate through time items 
      for time in class_time: 
        # iterate through days, find matching day times 
        days = re.findall('[A-Z]+', time)[0]
        print "days" + days
        print list(days)
        for day in days: 
            if (day == self_day): 
                print "current day: " + day
                # matching day, extract stime/etime
                times = re.sub('[A-Z]+', '', time).split(':')
                stime = int(times[0])
                etime = int(times[1])
                print "stime: " + str(stime) + " etime: " + str(etime)
                # check if stime/etime not conflicting with self stime/etime
                if (not ((self_etime < stime) or (self_stime > etime))): 
                    # conflicting times
                    print "conflict"
                    return False
    print "no conflict"

    #print schedule_model_data
    return schedule_model_data

