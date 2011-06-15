# Find Metal Albums

This package is intended to find about new releases of heavy metal
albums, and add relevant releases to a calendar in *Google Calendar*
as events.

## Components

The program is launched via the _launcher.py_ file. Relevant modules
are:

### Finder

Generates a list of interesting bands. This is done by parsing a
folder (i.e the iTunes Music Folder) and storing each folder, which
represents a group, as a line in a file.

### Scrapper

Parses a [http://en.wikipedia.org](Wikipedia) page which contains the
new releases for metal bands in a given year. Relevant albums, which
are the ones from groups obtained in the previous step, are stored, as
well as the release date and band name.

### Notifier

Connects to *Google Calendar* and creates (or updates) a new event for
each result of the _Scrapper_.

## Limitations:

1. An existing Calendar has to be used. Its Id has to be specified in
the config file.

2. For security reasons, neither the username or the password for the
Google account are stored, and have to be provided on each run. For
this reason, the program it is not suitable for a cronjob. If there is
a better solution for this, I'd love to hear about it.


