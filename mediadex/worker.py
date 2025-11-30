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
from mediadex.exc import BackendException, ConfigException
from mediadex.item import Item, Family


LOG = logging.getLogger(__name__)


class Worker:
    def __init__(self, config):
        '''
        Create Worker object from Config object
        '''

        LOG.debug(f"Worker configuration: {config}")
        self.config = config

        self.opensearch = None
        self.arangodb = None

    def work(self):
        '''
        Connect to backends and walk the filesystem
        '''
        LOG.info("Starting")

        # Get working directories from config
        movies_paths = self.config.settings["paths"]["movies"]
        music_paths = self.config.settings["paths"]["music"]
        shows_paths = self.config.settings["paths"]["shows"]

        # Check for working directories
        if len(movies_paths) + len(music_paths) + len(shows_paths) == 0:
            LOG.error("No media paths configured, aborting")
            raise ConfigException

        try:
            # Connect to ArangoDB backend
            if len(self.config.settings["arangodb"]["hosts"]) > 0:
                self.arangodb = arangodb.Client(self.config.settings["arangodb"])

            # Connect to OpenSearch backend
            if len(self.config.settings["opensearch"]["hosts"]) > 0:
                self.opensearch = opensearch.Client(self.config.settings["opensearch"])

        except Exception as exc:
            LOG.exception(f"Failure connecting to backends: {exc}")
            raise BackendException(exc)

        # Check for a backend connection
        if self.arangodb is None and self.opensearch is None:
            LOG.error("No backend configured, aborting")
            raise ConfigException

        # Walk each path
        for path in self.config.settings['paths']['movies']:
            LOG.debug(f"Walking path: {path}")
            self.walk_path(path, Family.MOVIES)

        for path in self.config.settings['paths']['music']:
            LOG.debug(f"Walking path: {path}")
            self.walk_path(path, Family.MUSIC)

        for path in self.config.settings['paths']['shows']:
            LOG.debug(f"Walking path: {path}")
            self.walk_path(path, Family.SHOWS)

    def walk_path(self, path, family):
        '''
        Walk the filesystem and index entries into backends
        '''
        for root, dirs, files in os.walk(path):
            for file in files:
                fullname = os.path.join(root, file)

                it = Item(family, fullname, file, path)

                try:
                    if self.arangodb:
                        # LOG.debug(f"Indexing {fullname} into ArangoDB")
                        self.arangodb.index(it)
                except Exception as exc:
                    LOG.error(f"Could not index {fullname} into ArangoDB")
                    LOG.exception(exc)

                try:
                    if self.opensearch:
                        # LOG.debug(f"Indexing {filename} into OpenSearch")
                        self.opensearch.index(it)
                except Exception as exc:
                    LOG.error(f"Could not index {fullname} into OpenSearch")
                    LOG.exception(exc)
