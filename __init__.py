'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Puppeteer",
    "description": "Automation for animation",
    "author": "Samy Tichadou (tonton)",
    "version": (0, 1, 0),
    "blender": (2, 91, 2),
    "location": "Sidebar > Puppeteer",
    "warning": "",
    "doc_url": "https://github.com/samytichadou/puppeteer_blender_addon",
    "tracker_url": "https://github.com/samytichadou/puppeteer_blender_addon/issues/new",
    "category": "Animation" }

import bpy


# IMPORT SPECIFICS
##################################

from . import   (
    addon_prefs,
    properties,
    gui,
    ui_lists,
    version_check,
)

from .operators import (
    automation_set_actions,
    automation_actions,
    create_automation,
    puppet_modal,
    check_new_version,
)


# register
##################################


def register():

    addon_prefs.register()
    properties.register()
    gui.register()
    ui_lists.register()
    version_check.register()

    automation_set_actions.register()
    automation_actions.register()
    create_automation.register()
    puppet_modal.register()
    check_new_version.register()

def unregister():

    addon_prefs.unregister()
    properties.unregister()
    gui.unregister()
    ui_lists.unregister()
    version_check.unregister()

    automation_set_actions.unregister()
    automation_actions.unregister()
    create_automation.unregister()
    puppet_modal.unregister()
    check_new_version.unregister()