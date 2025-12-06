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

from arango import ArangoClient

from mediadex.item import Family


LOG = logging.getLogger(__name__)


class Client:
    def __init__(self, config):
        self.config = config

        self.upstream_client = None

        self.database = None
        self.collections = {
            Family.MOVIES: None,
            Family.MUSIC: None,
            Family.SHOWS: None,
        }

    def connect(self):
        '''
        Connect to ArangoDB
        '''
        LOG.info("Connecting to ArangoDB")
        self.upstream_client = ArangoClient(hosts=self.config["hosts"])

        self.database = self.upstream_client.db(
            self.config["database"],
            username=self.config["username"],
            password=self.config["password"],
        )

        if self.config["collection_prefix"]:
            movies_collection = f"{self.config['collection_prefix']}-{Family.MOVIES}"
            music_collection = f"{self.config['collection_prefix']}-{Family.MUSIC}"
            shows_collection = f"{self.config['collection_prefix']}-{Family.SHOWS}"
        else:
            movies_collection = Family.MOVIES
            music_collection = Family.MUSIC
            shows_collection = Family.SHOWS

        if self.database.has_collection(movies_collection):
            self.collections[Family.MOVIES] = self.database.collection(movies_collection)
        else:
            self.collections[Family.MOVIES] = self.database.create_collection(movies_collection)

        if self.database.has_collection(music_collection):
            self.collections[Family.MUSIC] = self.database.collection(music_collection)
        else:
            self.collections[Family.MUSIC] = self.database.create_collection(music_collection)

        if self.database.has_collection(shows_collection):
            self.collections[Family.SHOWS] = self.database.collection(shows_collection)
        else:
            self.collections[Family.SHOWS] = self.database.create_collection(shows_collection)

    def index(self, it):
        '''
        Index an Item into ArangoDB
        '''
        # Connect to client, if needed
        if self.upstream_client is None:
            self.connect()

        # check for existing entry
        if self.collections[it.family].has(it.fingerprint):
            LOG.debug(f"Skipping exsting document: {it.fingerprint}")
            return

        # insert document into collection
        LOG.info(f"Indexing {it.fullpath} into ArangoDB")
        document = it.document
        document["_key"] = it.fingerprint
        self.collections[it.family].insert(document)
