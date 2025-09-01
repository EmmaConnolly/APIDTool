#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C)    2025 Emma Connolly
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

register(TOOL,
         id = 'APIDTool',
         name = _("Fix blank Ancestry.com citations"),
         description = _("Fills in the source and volume/page fields of blank Ancestry.com citations with the _APID for easier editing and merging."),
         version = '0.0.0',
         gramps_target_version = '6.0',
         status = EXPERIMENTAL,
         fname = 'apidtool.py',
         authors = ["Emma Connolly"],
         authors_email = ["emconnolly72@mailfence.com"],
         category = TOOL_DBPROC,
         toolclass = 'APIDTool',
         optionclass = 'APIDToolOptions',
         tool_modes = [TOOL_MODE_GUI]
         )
