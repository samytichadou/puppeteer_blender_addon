import bpy
import blf


from .. import event_list
from ..addon_prefs import get_addon_preferences
from ..gui import return_active_set_automation


# draw text line from fontid
def draw_text_line(font_id, right_pos, up_pos, text):
    blf.position(font_id, right_pos, up_pos, 0)
    blf.draw(font_id, text)


# draw puppet helper
def draw_puppet_helper_callback_px(self, context):
    font_id = 0  # XXX, need to find out how best to get this.
    
    prefs = get_addon_preferences()
    col = prefs.ui_text_color
    size = prefs.ui_text_size

    props = context.scene.pupt_properties
    paste_mode = props.paste_mode
    a_set, a_automation = return_active_set_automation(context)
    
    if self._modifier_shift:
        keyframing_mode = "ADDITIVE"
    else:
        keyframing_mode = "NORMAL"

    size_coef = size/14

    line_offset = int(15 * size_coef)

    # right margin
    right_mg = 15

    blf.color(0, *col)
    blf.size(font_id, size, 72)

    l_pos = 15
    draw_text_line(font_id, right_mg, l_pos, "Puppeteer    H - Toggle Help")

    if self.show_help:
        
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
        draw_text_line(font_id, right_mg, l_pos, "Shift - Additive Keyframing")
        l_pos += line_offset
        draw_text_line(font_id, right_mg, l_pos, "Down Arrow - Automation Set")
        l_pos += line_offset
        draw_text_line(font_id, right_mg, l_pos, "Up Arrow - Paste Mode")

        l_pos += 5
        for a in reversed(a_set.automation):
            if a.key_assignment != "NONE":
                l_pos += line_offset
                blf.position(font_id, right_mg, l_pos, 0)
                blf.draw(font_id, "%s - %s" % (a.key_assignment, a.name))


def change_active_set(context):

    props = context.scene.pupt_properties
    idx = props.automation_set_index
    
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


def set_properties_from_parent(parent, keyframe, dimension):

    if dimension == 0:
        value = keyframe.fcurve_value
    else:
        value = getattr(parent, keyframe.fcurve_data_path)
        value[keyframe.fcurve_array_index] = keyframe.fcurve_value
    
    return value


def set_additive_properties_from_parent(parent, keyframe, dimension):
    
    if dimension == 0:
        value = getattr(parent, keyframe.fcurve_data_path) + keyframe.fcurve_additive_value
    else:
        value = getattr(parent, keyframe.fcurve_data_path)
        value[keyframe.fcurve_array_index] += keyframe.fcurve_additive_value

    return value


def create_keyframe_from_parent(keyframe, current_frame, additive):

    if not keyframe.parent_name:
        return

    # get direct parent
    if keyframe.parent_type == "OBJECT":
        parent = bpy.data.objects[keyframe.parent_name]
    elif keyframe.parent_type == "MATERIAL":
        parent = bpy.data.materials[keyframe.parent_name]
    elif keyframe.parent_type == "WORLD":
        parent = bpy.data.worlds[keyframe.parent_name]
    # nodes
    elif keyframe.parent_type in {"MATERIAL_NTREE", "WORLD_NTREE"}:
        if keyframe.parent_type == "MATERIAL_NTREE":
            parent = bpy.data.materials[keyframe.parent_name].node_tree
        elif keyframe.parent_type == "WORLD_NTREE":
            parent = bpy.data.worlds[keyframe.parent_name].node_tree
        if keyframe.socket_type == "INPUTS":
            parent = parent.nodes[keyframe.node_name].inputs[keyframe.socket_index]
        else:
            parent = parent.nodes[keyframe.node_name].outputs[keyframe.socket_index]
    # pose
    elif keyframe.parent_type == "OBJECT_POSE":
        parent = bpy.data.objects[keyframe.parent_name].pose.bones[keyframe.bone_name]

    # set value for the keyframes additive and normal
    dim = parent.bl_rna.properties[keyframe.fcurve_data_path].array_length

    if not additive:
        value = set_properties_from_parent(parent, keyframe, dim)
    else:
        value = set_additive_properties_from_parent(parent, keyframe, dim)
    setattr(parent, keyframe.fcurve_data_path, value)

    # set kframes
    if dim == 0:
        parent.keyframe_insert(
            keyframe.fcurve_data_path,
            frame = current_frame + keyframe.fcurve_frame,
            )
    else:
        parent.keyframe_insert(
            keyframe.fcurve_data_path,
            index = keyframe.fcurve_array_index,
            frame = current_frame + keyframe.fcurve_frame,
            )


class PUPT_OT_Puppet_Modal(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "pupt.puppet_modal"
    bl_label = "Puppet"
    bl_options = {"UNDO"} #, "INTERNAL"}

    _modifier_shift = False
    _event = None

    show_help : bpy.props.BoolProperty(default = True)

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
            if props.paste_mode == "PARENT":
                create_keyframe_from_parent(kf, current_frame, self._modifier_shift)

        for area in context.screen.areas:
            area.tag_redraw()


    def modal(self, context, event):
        context.area.tag_redraw()
        
        # special shortcuts
        if event.type in event_list.shortcut_event and event.value == "PRESS":
            # ESC
            if event.type == 'ESC':
                self.finish(context)
                return {'FINISHED'}
            # SPACE
            elif event.type == 'SPACE':
                if not context.screen.is_animation_playing:
                    bpy.ops.screen.animation_play()
                else:
                    bpy.ops.screen.animation_cancel(restore_frame = False)
            # DWN ARROW
            elif event.type == "DOWN_ARROW":
                change_active_set(context)
            # UP ARROW
            elif event.type == "UP_ARROW":
                change_paste_mode(context)
            # H
            elif event.type == "H":
                self.show_help = not self.show_help

        # action
        elif event.type in event_list.used_event and event.value == "PRESS":
            self._event = event.type
            self.execute(context)

        # modifiers
        elif event.type in event_list.modifier_event:
            # SHIFT modifier
            if event.type in {"LEFT_SHIFT", "RIGHT_SHIFT"}:
                if event.value == "PRESS":
                    self._modifier_shift = True
                elif event.value == "RELEASE":
                    self._modifier_shift = False

        # passtrough
        elif event.type in event_list.passthrough_event:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}


    def invoke(self, context, event):
        # check for 3d viewport context
        if context.space_data.type != "VIEW_3D":
            self.report({"WARNING"}, "Active space must be a View3d")
            return {"CANCELLED"}

        # draw
        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_puppet_helper_callback_px, args, 'WINDOW', 'POST_PIXEL')

        # modal
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def finish(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Puppet_Modal)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Puppet_Modal)