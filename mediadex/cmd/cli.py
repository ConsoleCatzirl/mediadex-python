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

import argparse
import logging
import pathlib


from mediadex.app.worker import Worker
from mediadex.config import Config

from ruamel.yaml import YAML


class CLI:
    def __init__(self):
        self.log = None
        self.args = None

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--verbose',
                            action='count', dest='verbose',
                            help='Increase verbosity')
        parser.add_argument('-c', '--config',
                            action='store', dest='config',
                            help='Path to config file')
        self.args = parser.parse_args()

    def setup_logging(self, level):
        root_log = logging.getLogger()
        root_log.setLevel(level)
        sh = logging.StreamHandler()
        sh.setLevel(level)
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        sh.setFormatter(logging.Formatter(fmt))
        root_log.addHandler(sh)

        self.log = logging.getLogger(__name__)
        self.log.setLevel(level)

    def read_config(self, path):
        conf = Config()

        if not path:
            self.log.debug("Default Configuration")
            return conf

        self.log.debug("Reading Config")

        reader = YAML(typ='safe')
        _path = pathlib.Path(path)
        yaml = reader.load(_path)

        conf.read_dict(yaml)
        return conf

    def run(self):
        self.parse_args()

        # Set up logging
        if self.args.verbose is None:
            self.setup_logging(level=logging.WARNING)
        elif self.args.verbose == 1:
            self.setup_logging(level=logging.INFO)
        else:
            self.setup_logging(level=logging.DEBUG)

        # Read configuration
        config = None
        try:
            config = self.read_config(self.args.config)
            if config is None:
                self.log.error("Failed to load config file")
                return 1
        except Exception as exc:
            self.log.exception(f"Failed to read config file: {exc}")
            return 1

        # Run Worker
        try:
            worker = Worker(config)
            worker.work()
        except Exception as exc:
            self.log.exception(f"Worker failed: {exc}")
            return 2

        # Clean exit
        return 0
