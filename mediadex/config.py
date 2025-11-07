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

import copy
import logging

from mediadex import util


LOG = logging.getLogger(__name__)


class Config:

    # default values
    defaults = {
        "paths": {
            "movies": [],
            "music": [],
            "shows": [],
        },
        "opensearch": {
            "hosts": [],
            "username": None,
            "password": None,
        },
        "arangodb": {
            "host": None,
            "port": None,
            "username": None,
            "password": None,
        },
    }

    def __init__(self):
        self.settings = copy.deepcopy(self.defaults)

    def __str__(self):
        return f"{self.settings}"

    def read_dict(self, config):
        LOG.debug(f"Configuration data: {config}")

        if not config:
            return

        self.settings = util.merge_dict(self.settings, config)
