import bpy
import socket
import json
import requests
import addon_utils

from bpy.app.handlers import persistent

addon_version_url = "https://raw.githubusercontent.com/samytichadou/puppeteer_blender_addon/master/addon_version.json"


# check for internet connection
def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print("Puppeteer --- Error : " + ex)
        return False


# read an online json
def read_online_json(url):
    file_object = requests.get(url)
    return file_object.json()


# get addon version 
def get_addon_version(addon_name):
    for addon in addon_utils.modules():
        if addon.bl_info['name'] == addon_name:
            addon_version = ""
            for n in addon.bl_info.get('version', (-1,-1,-1)):
                addon_version += str(n) + "."
            addon_version = addon_version[:-1]
            return addon_version
    return None


# clear update props
def clear_update_properties(pupt_properties):
    pupt_properties.update_needed = False
    pupt_properties.update_message = ""
    pupt_properties.update_download_url = ""


# check for addon new version
def check_addon_version():

    print("Puppeteer --- Checking for new version")

    props = bpy.context.scene.pupt_properties
    
    if not is_connected():
        clear_update_properties(props)
        return False

    new_addon_infos = read_online_json(addon_version_url)

    if new_addon_infos["version"] != get_addon_version("Puppeteer"):
        props.update_message = new_addon_infos["message"]
        props.update_download_url = new_addon_infos["download_url"]
        props.update_needed = True
        return True
    else:
        clear_update_properties(props)

    return True


# startup handler function
@persistent
def pupt_startup_check_version(scene):
    check_addon_version()


### REGISTER ---

def register():
    bpy.app.handlers.load_post.append(pupt_startup_check_version)

def unregister():
    bpy.app.handlers.load_post.remove(pupt_startup_check_version)