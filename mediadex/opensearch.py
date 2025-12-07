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

from mediadex.item import Family

from opensearchpy import OpenSearch

LOG = logging.getLogger(__name__)


class Client:
    def __init__(self, config):
        self.config = config

        self.upstream_client = None

        self.indices = {
            Family.MOVIES: None,
            Family.MUSIC: None,
            Family.SHOWS: None,
        }

    def connect(self):
        '''
        Connect to OpenSearch
        '''
        LOG.info("Connecting to OpenSearch")
        self.upstream_client = OpenSearch(
            hosts=self.config["hosts"],
            verify_certs=self.config["secure"],
            http_auth=(
                self.config["username"],
                self.config["password"],
            ),
        )

        if self.config["index_prefix"]:
            self.indices[Family.MOVIES] = f"{self.config['index_prefix']}-{Family.MOVIES}"
            self.indices[Family.MUSIC] = f"{self.config['index_prefix']}-{Family.MUSIC}"
            self.indices[Family.SHOWS] = f"{self.config['index_prefix']}-{Family.SHOWS}"
        else:
            self.indices[Family.MOVIES] = Family.MOVIES
            self.indices[Family.MUSIC] = Family.MUSIC
            self.indices[Family.SHOWS] = Family.SHOWS

        if not self.upstream_client.indices.exists(self.indices[Family.MOVIES]):
            self.upstream_client.indices.create(self.indices[Family.MOVIES])

        if not self.upstream_client.indices.exists(self.indices[Family.MUSIC]):
            self.upstream_client.indices.create(self.indices[Family.MUSIC])

        if not self.upstream_client.indices.exists(self.indices[Family.SHOWS]):
            self.upstream_client.indices.create(self.indices[Family.SHOWS])

    def index(self, it):
        '''
        Index an Item into OpenSearch
        '''
        if self.upstream_client is None:
            self.connect()

        exists = self.upstream_client.exists(index=self.indices[it.family], id=it.fingerprint)
        if exists:
            if self.config["force"]:
                LOG.debug(f"Forcing re-indexing: {it.fingerprint}")
            else:
                LOG.debug(f"Skipping exsting document: {it.fingerprint}")
                return

        if self.config["dryrun"]:
            LOG.debug(f"Dry run, not indexing {it.fullpath}")
        else:
            if exists:
                LOG.info(f"Updating {it.fullpath} into OpenSearch")
                self.upstream_client.update(index=self.indices[it.family], id=it.fingerprint, body=it.document)
            else:
                LOG.info(f"Indexing {it.fullpath} into OpenSearch")
                self.upstream_client.create(index=self.indices[it.family], id=it.fingerprint, body=it.document)
