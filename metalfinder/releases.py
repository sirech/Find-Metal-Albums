import urllib2
import os
import codecs
import datetime
import re

from BeautifulSoup import BeautifulSoup

from existing import process_band_name

def create_opener():
    '''
    Creates an url opener that has its User-Agent set to Mozilla.
    '''
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    return opener

BASE_URL = 'http://en.wikipedia.org/wiki/%d_in_heavy_metal_music'

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

CITATION = r'\[\d+\]$'

def url_for_current_year():
    '''
    Gets the url for the page from where the albums are scrapped for the current year.
    '''
    return BASE_URL % (datetime.datetime.now().year)

def remove_citation(s):
    '''Remove the citation (wikipedia-style) of the given string.'''
    return re.sub(CITATION, '', s)

def month_as_number(month):
    '''Returns the month, which has to be a member of the MONTHS list,
    as number in the range [1,12]'''
    return MONTHS.index(month) + 1

class Scrapper(object):
    '''
    This class is responsible for scrapping a Wikipedia page which
    contains all the planned releases for a year. The page is parsed
    with help of BeautifulSoup, and then a list of entries is produced
    with all the albums and bands.

    If there is a existing file with names of bands, only releases of
    these bands are included in the output.
    '''

    def __init__(self, config):
        self._cfg = config
        self._existing = self._load_existing()
        self._opener = create_opener()

    def _load_existing(self):
        '''
        Loads the existing bands as a set from a file. If the file
        does not exist, an empty set is returned.
        '''
        path = os.path.expanduser(self._cfg['existing_file'])

        if os.path.exists(path):
            f = codecs.open(path, 'r', 'utf-8')
            return set(line.strip() for line in f.readlines())
        else:
            return set()

    @property
    def albums(self):
        '''Gets the albums for the current year.

        The result is a list with a tuple for each month like this:

        [('January', *result of albums for Jan*),
        ('February', *result of albums for Feb*),
        ...
        ]
        '''
        soup = self._soupify(url_for_current_year())
        albums = []
        for month in MONTHS:
            albums.append(tuple([month, self._albums_for_month(soup, month)]))
        return albums

    def _soupify(self, url):
        '''Returns a soup object of the given url.'''
        return BeautifulSoup(self._opener.open(url))

    def _albums_for_month(self, soup, month):
        '''
        Find all the albums to be released in a given month. To do
        this, the heading for the month is retrieved. Right after it
        is the table with the data. Only the albums from groups in the
        _existing set are included.

        The result is a list of tuples, like this:

        [('Metallica', 'Master of Puppets', 15), ('AFI', 'Sing the Sorrow', 23)]

        soup the soup object used to scrap the site

        month the month to search for, which is an entry in MONTHS
        '''
        prev = soup.find('span', id=month).parent
        entries = prev.findNextSibling('table').findAll('tr')
        albums = []
        day = None
        for entry in list(entries)[1:]:
            rows = [row.text for row in entry.findAll('td')]

            # Some entries include the day and some not
            if len(rows) == 3:
                day, band, album = rows
            elif len(rows) == 2:
                band, album = rows
            else:
                continue

            if len(self._existing) == 0 or process_band_name(band) in self._existing:
                albums.append(tuple([band, remove_citation(album), int(day)]))
        return albums
