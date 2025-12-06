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
import os
import stat

from mediadex import fingerprint, mediainfo


LOG = logging.getLogger(__name__)


class Family:
    MOVIES = "movies"
    MUSIC = "music"
    SHOWS = "shows"


class Item:
    def __init__(self, family, fullpath, basename, basedir):
        self.family = family
        self.fullpath = fullpath
        self.basename = basename
        self.basedir = basedir

        self._filestat = None
        self._fingerprint = None
        self._mediainfo = None

    @property
    def filesize(self):
        if self._filestat is None:
            self._filestat = os.lstat(self.fullpath)
        return self._filestat.st_size

    @property
    def is_regular(self):
        if self._filestat is None:
            self._filestat = os.lstat(self.fullpath)
        return stat.S_ISREG(self._filestat.st_mode)

    @property
    def fingerprint(self):
        if self._fingerprint is None:
            self._fingerprint = fingerprint.generate(self.fullpath)
        return self._fingerprint

    @property
    def mediainfo(self):
        if self._mediainfo is None:
            self._mediainfo = mediainfo.generate(self.fullpath)
        return self._mediainfo

    @property
    def document(self):
        return {
            "fileinfo": {
                "filesize": self.filesize,
                "fullpath": self.fullpath,
                "basename": self.basename,
                "basedir": self.basedir,
                "checksum": self.fingerprint,
            },
            "mediainfo": self.mediainfo,
        }
