import bpy
import blf


from .. import event_list
from ..addon_prefs import get_addon_preferences
from ..gui import return_active_set_automation
from .automation_set_actions import get_unique_name


# draw text line from fontid
def draw_text_line(font_id, right_pos, up_pos, text):
    blf.position(font_id, right_pos, up_pos, 0)
    blf.draw(font_id, text)


# draw puppet helper
def draw_puppet_helper_callback_px(self, context):
    font_id = 0
    
    prefs = get_addon_preferences()
    col = prefs.ui_text_color
    size = prefs.ui_text_size

    props = context.scene.pupt_properties
    paste_mode = props.paste_mode
    a_set, a_automation = return_active_set_automation(context)
    
    if props.additive_keyframing:
        keyframing_mode = "ADDITIVE"
    else:
        keyframing_mode = "NORMAL"

    size_coef = size/14

    line_offset = int(15 * size_coef)

    # right margin
    right_mg = self._mouse_x

    blf.color(0, *col)
    blf.size(font_id, size, 72)

    l_pos = self._mouse_y
    draw_text_line(font_id, right_mg, l_pos, "Puppeteer    H - Toggle Help")

    if self._show_help:
        
        l_pos += 5
        l_pos += line_offset
        draw_text_line(font_id, right_mg, l_pos, "Paste Mode - %s" % paste_mode)
        l_pos += line_offset
        draw_text_line(font_id, right_mg, l_pos, "Puppet Set - %s" % a_set.name)
        l_pos += line_offset
        draw_text_line(font_id, right_mg, l_pos, "Keyframing - %s" % keyframing_mode)

        l_pos += 5
        l_pos += line_offset
        draw_text_line(font_id, right_mg, l_pos, "Esc/Enter - Quit")
        l_pos += line_offset
        draw_text_line(font_id, right_mg, l_pos, "Alt R - Move Help")
        l_pos += line_offset
        draw_text_line(font_id, right_mg, l_pos, "Alt L - Additive Keyframing")
        l_pos += line_offset
        draw_text_line(font_id, right_mg, l_pos, "Up/Down - Automation Set")
        l_pos += line_offset
        draw_text_line(font_id, right_mg, l_pos, "Tab - Paste Mode")

        l_pos += 5
        for a in reversed(a_set.automation):
            if a.key_assignment != "NONE":
                l_pos += line_offset
                blf.position(font_id, right_mg, l_pos, 0)
                blf.draw(font_id, "%s - %s" % (a.key_assignment, a.name))


def change_active_set(context, direction):

    props = context.scene.pupt_properties
    idx = props.automation_set_index
    
    if direction == "up":
        if idx == 0:
            props.automation_set_index = len(props.automation_set) - 1
        else:
            props.automation_set_index -= 1

    elif direction == "dwn":
        if idx < len(props.automation_set) - 1:
            props.automation_set_index += 1
        elif idx == len(props.automation_set) - 1:
            props.automation_set_index = 0


def change_paste_mode(context):
    
    props = context.scene.pupt_properties

    # init prop if needed
    try:
        paste_mode = props["paste_mode"]
    except KeyError:
        props.paste_mode = props.paste_mode
        paste_mode = props["paste_mode"]

    if paste_mode < 2:
        props["paste_mode"] += 1
    else:
        props["paste_mode"] = 0


# get parent object from name
def get_parent_object(parent_type, parent_name):
    parent = None

    if parent_type == "OBJECT":
        try:
            parent = bpy.data.objects[parent_name]
        except KeyError:
            return parent
    elif parent_type == "MATERIAL":
        try:
            parent = bpy.data.materials[parent_name]
        except KeyError:
            return parent
    elif parent_type == "WORLD":
        try:
            parent = bpy.data.worlds[parent_name]
        except KeyError:
            return parent
    # nodes
    elif parent_type in {"MATERIAL_NTREE", "WORLD_NTREE"}:
        if parent_type == "MATERIAL_NTREE":
            try:
                parent = bpy.data.materials[parent_name].node_tree
            except KeyError:
                return parent
        elif parent_type == "WORLD_NTREE":
            try:
                parent = bpy.data.worlds[parent_name].node_tree
            except KeyError:
                return parent
    
    return parent


# get fcurve from parent object
def get_fcurve_parent(parent, data_path, array_index, group):

    fc = None

    if parent.animation_data is None:
        parent.animation_data_create()
    a_d = parent.animation_data

    if a_d.action is None:
        new_name = get_unique_name(bpy.data.actions, parent.name + "Action")
        a_d.action = bpy.data.actions.new(new_name)

    fc = a_d.action.fcurves.find(data_path, index = array_index)
    if fc is None:
        fc = a_d.action.fcurves.new(data_path, index = array_index, action_group = group)

    return fc


# get fcurve from action name
def get_fcurve_action(action_name, data_path, array_index, group):
    
    fc = None
    
    for act in bpy.data.actions:
        if act.name == action_name:
            fc = act.fcurves.find(data_path, index = array_index)
            if fc is None:
                fc = act.fcurves.new(data_path, index = array_index, action_group = group)
            break

    return fc


# get fcurve from parent and action
def get_fcurve_parent_action(parent, action_name, data_path, array_index, group):

    fc = None

    if parent.animation_data is None:
        parent.animation_data_create()
    a_d = parent.animation_data

    if a_d.action is not None:
        if a_d.action.name == action_name:
            fc = a_d.action.fcurves.find(data_path, index = array_index)
            if fc is None:
                fc = a_d.action.fcurves.new(data_path, index = array_index, action_group = group)

    return fc


# create and set keyframe
def set_keyframe(fcurve, value, keyframe_from_coll, current_frame):

    new_key = fcurve.keyframe_points.insert(
        current_frame + keyframe_from_coll.fcurve_frame,
        value
        )

    new_key.handle_left[0] = current_frame + keyframe_from_coll.handle_left[0]
    new_key.handle_left[1] = value + keyframe_from_coll.handle_left[1]
    new_key.handle_left_type = keyframe_from_coll.handle_left_type
    new_key.handle_right[0] = current_frame + keyframe_from_coll.handle_right[0]
    new_key.handle_right[1] = value + keyframe_from_coll.handle_right[1]
    new_key.handle_right_type = keyframe_from_coll.handle_right_type


def set_keyframe_from_paste_mode(keyframe, current_frame, additive, paste_mode):
    
    debug = get_addon_preferences().debug

    if paste_mode in {"PARENT", "PARENT_ACTION"}:

        if not keyframe.parent_name:
            if debug: print("Puppeteer --- Skip keyframe without parent name") #debug
            return False

        if debug: print("Puppeteer --- Pasting keyframe") #debug

        # get parent   
        parent = get_parent_object(keyframe.parent_type, keyframe.parent_name)
        
        if parent is None:
            if debug: print("Puppeteer --- Skip keyframe, unable to find parent") #debug
            return False

        if debug: print("Puppeteer --- Parent to paste %s" % parent.name) #debug

        # find fcurve
        if paste_mode == "PARENT":
            fc = get_fcurve_parent(
                parent, 
                keyframe.fcurve_data_path, 
                keyframe.fcurve_array_index, 
                keyframe.fcurve_group
                )

        elif paste_mode == "PARENT_ACTION":
            fc = get_fcurve_parent_action(
                parent, 
                keyframe.action_name, 
                keyframe.fcurve_data_path, 
                keyframe.fcurve_array_index, 
                keyframe.fcurve_group
                )

    elif paste_mode == "ACTION":

        # find fcurve
        fc = get_fcurve_action(keyframe.action_name, keyframe.fcurve_data_path, keyframe.fcurve_array_index, keyframe.fcurve_group)

    if fc is None:
        if debug: print("Puppeteer --- Skip keyframe, unable to find FCurve") #debug
        return False
    
    if debug: print("Puppeteer --- Fcurve to paste %s" % fc.data_path) #debug

    # process value
    if additive:
        value = fc.evaluate(current_frame) + keyframe.fcurve_additive_value
    else:
        value = keyframe.fcurve_value

    if debug: print("Puppeteer --- Value to paste %f" % value) #debug

    if debug: print("Puppeteer --- Setting keyframe") #debug

    set_keyframe(fc, value, keyframe, current_frame)

    if debug: print("Puppeteer --- Keyframe set") #debug

    return True


class PUPT_OT_Puppet_Modal(bpy.types.Operator):
    """Animate through assigned shortcut"""
    bl_idname = "pupt.puppet_modal"
    bl_label = "Puppet"
    bl_options = {"UNDO"} #, "INTERNAL"}

    _event = None

    _move_modifier = False
    _mouse_x = 15
    _mouse_y = 15

    _show_help = True

    @classmethod
    def poll(cls, context):
        if context.space_data.type == "VIEW_3D":
            a_set, a_automation = return_active_set_automation(context)
            return a_set is not None 


    def execute(self, context):
        props = context.scene.pupt_properties
        a_set, a_automation = return_active_set_automation(context)
        current_frame = context.scene.frame_current

        automation = None

        for a in a_set.automation:
            if a.key_assignment == self._event:
                automation = a
                break

        if automation is None:
            return

        for kf in automation.keyframe:
            chk_paste = True
            chk_paste = set_keyframe_from_paste_mode(kf, current_frame, props.additive_keyframing, props.paste_mode)

            if not chk_paste:
                print("Puppeteer --- Unable to paste keyframe")

        for area in context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "%s Automation Applied" % automation.name)


    def modal(self, context, event):
        context.area.tag_redraw()
        props = context.scene.pupt_properties
        
        # special shortcuts
        if event.type in event_list.shortcut_event:
            # ESC
            if event.type == 'ESC' and event.value == "PRESS":
                self.finish(context)
                return {'FINISHED'}
            # SPACE
            elif event.type == 'SPACE' and event.value == "PRESS":
                if not context.screen.is_animation_playing:
                    bpy.ops.screen.animation_play()
                else:
                    bpy.ops.screen.animation_cancel(restore_frame = False)
            # DWN ARROW
            elif event.type == "DOWN_ARROW" and event.value == "PRESS":
                change_active_set(context, "dwn")
            # UP ARROW
            elif event.type == "UP_ARROW" and event.value == "PRESS":
                change_active_set(context, "up")
            # H
            elif event.type == "H" and event.value == "PRESS":
                self._show_help = not self._show_help
            # TAB
            elif event.type == "TAB" and event.value == "PRESS":
                change_paste_mode(context)
            # ALT LEFT
            elif event.type == "LEFT_ALT":
                # toggle additive
                if get_addon_preferences().hold_additive:
                    # hold shift to additive
                    if event.value == "PRESS":
                        props.additive_keyframing = True
                    elif event.value == "RELEASE":
                        props.additive_keyframing = False
                else:
                    if event.value == "PRESS":
                        props.additive_keyframing = not props.additive_keyframing
            # ALT RIGHT
            elif event.type == "RIGHT_ALT":
                if event.value == "PRESS":
                    self._move_modifier = True
                    self._mouse_x = event.mouse_region_x
                    self._mouse_y = event.mouse_region_y
                elif event.value == "RELEASE":
                    self._move_modifier = False

        # action
        elif event.type in event_list.used_event and event.value == "PRESS":
            self._event = event.type
            self.execute(context)

        # mouse move
        elif self._move_modifier and event.type == 'MOUSEMOVE':
            self._mouse_x = event.mouse_region_x
            self._mouse_y = event.mouse_region_y

        # passtrough
        elif event.type in event_list.passthrough_event:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}


    def invoke(self, context, event):
        # check for 3d viewport context
        if context.space_data.type != "VIEW_3D":
            self.report({"WARNING"}, "Active space must be a View3d")
            return {"CANCELLED"}

        # reset additive if needed
        if get_addon_preferences().hold_additive:
            self._old_additive = context.scene.pupt_properties.additive_keyframing
            context.scene.pupt_properties.additive_keyframing = False

        # draw
        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_puppet_helper_callback_px, args, 'WINDOW', 'POST_PIXEL')

        # modal
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}


    def finish(self, context):
        if get_addon_preferences().hold_additive:
            context.scene.pupt_properties.additive_keyframing = self._old_additive
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Puppet_Modal)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Puppet_Modal)