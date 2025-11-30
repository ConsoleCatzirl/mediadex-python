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

import hashlib
import logging


LOG = logging.getLogger(__name__)


def generate(filepath):
    fingerprint = None
    with open(filepath, 'rb') as f:
        fingerprint = _generate(f)
        LOG.debug(f"Fingerprint for {filepath}: {fingerprint}")
    return fingerprint


def _generate(filelike):
    # Magic numbers for file chunking
    chunk_size = 24576
    chunk_count = 128

    hasher = hashlib.sha384()

    try:
        for _ in range(chunk_count):
            chunk = filelike.read(chunk_size)
            if chunk:
                hasher.update(chunk)
    except Exception as exc:
        if LOG.isEnabledFor(logging.INFO):
            LOG.exception(exc)
        else:
            LOG.warn(str(exc))

    return hasher.hexdigest()
