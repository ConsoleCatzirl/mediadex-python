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


LOG = logging.getLogger(__name__)


def merge_dict(main, update):
    if not update:
        return main

    for key in main.keys():
        if key not in update:
            # no updated value
            continue

        main_type = type(main[key])
        update_type = type(update[key])

        if main_type is not update_type:
            if update_type is not type(None):
                LOG.warning(f"Type mismatch: {update_type} "
                            f"is not {main_type}")
            continue

        if main_type is dict:
            main[key] = merge_dict(main[key], update[key])

        else:
            main[key] = update[key]

    return main
