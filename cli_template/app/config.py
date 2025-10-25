#  Python CLI Template
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


class Config:
    def __init__(self):
        self.log = logging.getLogger(__name__)

        # default values
        self.settings = {
            "option1": "foo",
            "option2": "bar",
        }

    def __str__(self):
        return f"{self.settings}"

    def read_dict(self, seed):
        self.log.debug(f"Configuration seed data: {seed}")

        if not seed:
            return

        for option in self.settings.keys():
            if option in seed:
                self.log.debug(f"Setting {option} to {seed[option]}")
                self.settings[option] = seed[option]
