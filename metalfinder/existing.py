# -*- coding: utf-8 -*-
import os
import codecs

def process_band_name(name):
    '''
    Removes whitespace, punctuation, letters with accents and upper
    case letters from a band name.
    '''
    assert isinstance(name, unicode)
    special = { u'á' : u'a',
                u'é' : u'e',
                u'í' : u'i',
                u'ó' : u'o',
                u'ú' : u'u',
                u'ñ' : u'ny' }
    name = name.lower()
    for letter, replacement in special.items():
        name = name.replace(letter, replacement)
    for invalid in ' .!?-_!,\'"':
        name = name.replace(invalid, '')
    return name

class Finder(object):
    '''
    Finds all the bands available on this computer. To do this, a
    folder where all the music is stored is specified. Each folder
    there is considered a band, identified by its name.
    '''

    def __init__(self, config):
        '''
        Loads the list of bands.
        '''
        self._cfg = config
        self._load_list()

    def _load_list(self):
        '''
        Every folder in the music folder is loaded as a band.
        '''
        path = os.path.expanduser(self._cfg['music_folder'])
        self._bands = sorted(set(process_band_name(f) for f in os.listdir(path)
                                 if os.path.isdir(os.path.join(path, f))))

    @property
    def bands(self):
        '''
        The list of bands as an iterator.
        '''
        return iter(self._bands)

    def to_file(self, fileName, folder='.'):
        '''
        Persists the list of bands to the given file, one band per line.
        '''
        path = os.path.expanduser(folder)
        f = codecs.open(os.path.join(path,fileName), 'w', 'utf-8')
        f.write('\n'.join(self.bands))
        f.close()
