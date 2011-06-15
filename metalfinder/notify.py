from datetime import datetime, timedelta
import json

import gdata
import gdata.calendar
import gdata.calendar.service

from releases import Scrapper, month_as_number

import logging
logger = logging.getLogger(__name__)

FORMAT= '%Y-%m-%d'

class Notifier(object):
    '''
    This class can connect to Google Calendar to create entries on obtained from the Scrapper.
    '''

    def __init__(self, config):
        self._cfg = config
        self._scrapper = Scrapper(config)
        self._date = datetime.now()

    def connect(self, user, password):
        '''
        Connects to Google Calendar according to the configuration.
        '''
        self._client = gdata.calendar.service.CalendarService()
        self._client.ClientLogin(user, password, source=app_name())

    def _uri_for_calendar(self):
        '''
        Gets the URI for the calendar to use. It has to be an existing calendar.
        '''
        return gdata.calendar.service.CalendarEventQuery(user=self._cfg['calendar_user'])

    def get_events(self):
        '''
        Gets the existing events in the calendar.

        The query is adapted to return entries that contain a given
        prefix. The time period is set between the actual time and the
        end of the current year.
        '''
        query = self._uri_for_calendar()
        query.text_query=self._cfg['entry_prefix']
        query.start_min = self._date.strftime(FORMAT)
        query.start_max = '%d-01-01' % (self._date.year + 1)
        # query.max_results = 100
        logger.debug('Getting events from the uri %s', query.ToUri())
        return self._client.GetCalendarEventFeed(query.ToUri())

    def _build_title(self, band, album):
        '''
        Returns the title to use for a entry for a given band and album.
        '''
        return '%s: %s -> %s' % (self._cfg['entry_prefix'], band, album)

    def _find_event(self, events, title):
        '''
        Finds an event with the given title by iterating over the
        given list of events. Returns None if no event is found.
        '''
        for event in events.entry:
            if event.title.text == title:
                return event
        return None

    def _add_or_edit_event(self, title, date, event):
        '''
        Adds an event with the given title to the calendar. If the
        event already exists, the existing one is adapted.

        The event is set as an all-day event, using the provided date.
        '''

        if event is None:
            logger.debug('Inserting new event')
            event = gdata.calendar.CalendarEventEntry()
            isNew = True
        else:
            logger.debug('Editing existing event')
            isNew = False

        event.title = gdata.atom.Title(text=title)
        start, end = date_and_next_day(date)
        event.when.append(gdata.calendar.When(
                start_time=start,
                end_time=end))
        print 'Commiting event... title: %s, starts:%s, ends:%s' % (
            event.title.text, event.when[0].start_time, event.when[0].end_time)
        logger.debug('Commiting event... title: %s, starts:%s, ends:%s',
                     event.title.text, event.when[0].start_time, event.when[0].end_time)
        if isNew:
            return self._clientInsertEvent(event, self._uri_for_calendar().ToUri(),
                                           { 'redirects_remaining' : 10 })
        else:
            return self._client.UpdateEvent(event.GetEditLink().href, event, { 'redirects_remaining' : 10 })

    def update_albums(self):
        '''
        Adds albums returned by the scrapper to the calendar.

        The albums that have a release date that is not in the past
        are added to the calendar. Every new album is searched in the
        list of events before inserting it, to avoid duplicates.
        '''
        albums = self._scrapper.albums
        events = self.get_events()

        for month, for_month in albums:
            for band, album, day in for_month:
                date = datetime(year=self._date.year, month=month_as_number(month), day=day)
                logger.debug('Processing... band: %s, album: %s, release:%s', band, album, date.strftime(FORMAT))
                if self._date < date:
                    title = self._build_title(band, album)
                    self._add_or_edit_event(title, date, self._find_event(events, title))


def date_and_next_day(date):
    '''
    Returns the given date and the one corresponding to the next day
    as a tuple of strings in the YYYY-MM-DD format.
    '''
    tomorrow = date + timedelta(days=1)
    return (date.strftime(FORMAT), tomorrow.strftime(FORMAT))

def app_name():
    '''
    Application name so that Google stays happy.
    '''
    name = json.load(open('manifest.json'))['name'].lower().replace(' ', '')
    return 'hceris-%s' % (name)
