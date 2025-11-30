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

import chardet
from pymediainfo import MediaInfo

LOG = logging.getLogger(__name__)


def generate(filepath):
    mediainfo = None

    try:
        mediainfo = _generate(filepath)

    except FileNotFoundError:
        _enc = filepath.encode('utf-8', 'surrogateescape')
        charset = chardet.detect(filepath).get('encoding')
        LOG.info(f"chardet found: {charset}")

        try:
            _f = _enc.decode(charset)
            mediainfo = _generate(_f)
        except FileNotFoundError:
            LOG.warning(f"chardet failure: {_f}")

    except Exception as exc:
        LOG.warning(str(exc))

    finally:
        if not mediainfo:
            _f = filepath.encode('utf-8', 'surrogateescape')
            raise IOError(f"Could not open {_f}")

    return mediainfo


def _generate(filepath):
    info = MediaInfo.parse(filepath)
    return info.to_data()
