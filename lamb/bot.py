import sys
"""
    Lamb - Light Ass Management Bot
    Copyright (C) 2020  github.com/griimnak

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__version__ = "0.0"
__author__ = "github.com/griimnak"

memory = {
    "active": False,
    "py_version": sys.version_info[:2],
    "lamb_version": __version__,
    "token": "",
    "command_prefix": "",
    "temp_dir": "",
    "cogs_dir": ""
}
