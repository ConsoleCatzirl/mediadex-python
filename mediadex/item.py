#  Mediadex Media Indexer
#  Copyright (C) 2025  Joni Harker

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging

from enum import Enum

from mediadex import fingerprint, mediainfo


LOG = logging.getLogger(__name__)


class Family(Enum):
    MOVIES = "movies"
    MUSIC = "music"
    SHOWS = "shows"


class Item:
    def __init__(self, family, filename):
        self.family = family
        self.filename = filename

        self._fingerprint = None
        self._mediainfo = None

    def get_fingerprint(self):
        if self._fingerprint is None:
            self._fingerprint = fingerprint.generate(self.filename)
        return self._fingerprint

    def get_mediainfo(self):
        if self._mediainfo is None:
            self._mediainfo = mediainfo.generate(self.filename)
        return self._mediainfo
