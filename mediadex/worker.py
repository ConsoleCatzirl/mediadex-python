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

from mediadex import arangodb, opensearch
from mediadex.item import Item, Family


LOG = logging.getLogger(__name__)


class Worker:
    def __init__(self, config):
        LOG.debug(f"Worker configuration: {config}")
        self.config = config

        self.opensearch = None
        self.arangodb = None

    def work(self):
        LOG.info("Starting")

        if self.config.settings["arangodb"]["host"] is not None:
            LOG.info("Connecting to ArangoDB")
            self.arangodb = arangodb.Client(
                    self.config.settings["arangodb"]
                )

        if len(self.config.settings["opensearch"]["hosts"]) > 0:
            LOG.info("Connecting to OpenSearch")
            self.opensearch = opensearch.Client(
                    self.config.settings["opensearch"]
                )

        if self.arangodb is None and self.opensearch is None:
            LOG.error("No backend configured, aborting")
            return

        movies_paths = self.config.settings["paths"]["movies"]
        music_paths = self.config.settings["paths"]["music"]
        shows_paths = self.config.settings["paths"]["shows"]

        if len(movies_paths) + len(music_paths) + len(shows_paths) == 0:
            LOG.error("No media paths configured, aborting")
            return

        for path in self.config.settings['paths']['movies']:
            self.walk_path(path, Family.MOVIES)

        for path in self.config.settings['paths']['music']:
            self.walk_path(path, Family.MUSIC)

        for path in self.config.settings['paths']['shows']:
            self.walk_path(path, Family.SHOWS)

    def walk_path(self, path, family):
        for root, dirs, files in os.walk(path):
            for file in files:
                filename = os.path.join(root, file)
                it = Item(family, filename)

                if self.arangodb:
                    LOG.info("Indexing into ArangoDB")
                    self.arangodb.index(it)

                if self.opensearch:
                    LOG.info("Indexing into OpenSearch")
                    self.opensearch.index(it)
