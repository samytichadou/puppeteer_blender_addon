import bpy
import blf


from .. import event_list
from ..addon_prefs import get_addon_preferences
from ..gui import return_active_set_automation


# draw puppet helper
def draw_puppet_helper_callback_px(self, context):
    font_id = 0  # XXX, need to find out how best to get this.
    
    prefs = get_addon_preferences()
    col = prefs.ui_text_color
    size = prefs.ui_text_size

    props = context.scene.pupt_properties
    paste_mode = props.paste_mode
    a_set, a_automation = return_active_set_automation(context)

    size_coef = size/14

    line_offset = int(16 * size_coef)

    # draw some text
    blf.color(0, *col)
    blf.size(font_id, size, 72)

    l_pos = 15
    blf.position(font_id, 15, l_pos, 0)
    blf.draw(font_id, "Puppet Set : " + a_set.name)

    l_pos += line_offset
    blf.position(font_id, 15, l_pos, 0)
    blf.draw(font_id, "Paste Mode : " + paste_mode)

    l_pos += line_offset
    blf.position(font_id, 15, l_pos, 0)
    blf.draw(font_id, "H - Help")

    if self.show_help:
        help_size = size - 3
        help_line_offset = int(13 * size_coef)

        blf.size(font_id, help_size, 72)

        l_pos += line_offset + 5
        blf.position(font_id, 15, l_pos, 0)
        blf.draw(font_id, "Esc/Enter - Quit")

        l_pos += help_line_offset
        blf.position(font_id, 15, l_pos, 0)
        blf.draw(font_id, "Up Arrow - Change Paste Mode")

        l_pos += help_line_offset
        blf.position(font_id, 15, l_pos, 0)
        blf.draw(font_id, "Down Arrow - Change Automation Set")

        l_pos += 5

        for a in a_set.automation:
            if a.key_assignment != "NONE":
                l_pos += help_line_offset
                blf.position(font_id, 15, l_pos, 0)
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
    

def create_keyframe_from_parent(keyframe, current_frame, additive):

    if not keyframe.parent_name:
        return

    if keyframe.parent_type == "OBJECT":
        parent = bpy.data.objects[keyframe.parent_name]
    elif keyframe.parent_type == "MATERIAL":
        parent = bpy.data.materials[keyframe.parent_name]
    elif keyframe.parent_type == "WORLD":
        parent = bpy.data.worlds[keyframe.parent_name]

    # set value for the keyframes additive and normal
    dim = parent.bl_rna.properties[keyframe.fcurve_data_path].array_length
    # normal
    if not additive:
        if dim == 0:
            value = keyframe.fcurve_value
        else:
            value = getattr(parent, keyframe.fcurve_data_path)
            value[keyframe.fcurve_array_index] = keyframe.fcurve_value
    # additive
    else:
        if dim == 0:
            value = getattr(parent, keyframe.fcurve_data_path) + keyframe.fcurve_additive_value
        else:
            value = getattr(parent, keyframe.fcurve_data_path)
            value[keyframe.fcurve_array_index] += keyframe.fcurve_additive_value
    setattr(parent, keyframe.fcurve_data_path, value)


    # set ntree kframes
    if dim == 0:
        parent.keyframe_insert(
            keyframe.fcurve_data_path,
            #index = keyframe.fcurve_array_index,
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

    show_help : bpy.props.BoolProperty()

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
                print("finished " + event.value)
                self.finish(context)
                return {'FINISHED'}
            # SPACE
            elif event.type == 'SPACE':
                print("space " + event.value)
                if not context.screen.is_animation_playing:
                    bpy.ops.screen.animation_play()
                else:
                    bpy.ops.screen.animation_cancel(restore_frame = False)
            # DWN ARROW
            elif event.type == "DOWN_ARROW":
                print("down " + event.value)
                change_active_set(context)
            # UP ARROW
            elif event.type == "UP_ARROW":
                print("up " + event.value)
                change_paste_mode(context)
            # H
            elif event.type == "H":
                print("H " + event.value)
                self.show_help = not self.show_help

        # action
        elif event.type in event_list.used_event and event.value == "PRESS":
            print(event.type)
            print("other " + event.value)
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
        print("finish function")
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Puppet_Modal)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Puppet_Modal)