import bpy
import blf

from .. import event_list
from ..addon_prefs import get_addon_preferences
from ..gui import return_active_set_automation
from .puppet_modal import draw_text_line


# draw puppet helper
def draw_key_assign_helper_callback_px(self, context):
    font_id = 0  # XXX, need to find out how best to get this.
    
    prefs = get_addon_preferences()
    col = prefs.ui_text_color
    size = prefs.ui_text_size

    size_coef = size/14
    line_offset = int(15 * size_coef)

    a_set, a_automation = return_active_set_automation(context)

    # right margin
    right_mg = 15

    blf.color(0, *col)
    blf.size(font_id, size, 72)

    l_pos = 15
    draw_text_line(font_id, right_mg, l_pos, "Esc/Mouse Click - Quit")

    l_pos += 5
    l_pos += line_offset
    draw_text_line(font_id, right_mg, l_pos, "Automation : %s" % a_automation.name)
    l_pos += line_offset
    draw_text_line(font_id, right_mg, l_pos, "Waiting for Keyboard Entry")


class PUPT_OT_Assign_Key(bpy.types.Operator):
    """Assign a key to active automation"""
    bl_idname = "pupt.assign_key"
    bl_label = "Assign Key"
    bl_options = {"UNDO", "INTERNAL"}

    _event = None

    @classmethod
    def poll(cls, context):
        if context.space_data.type == "VIEW_3D":
            a_set, a_automation = return_active_set_automation(context)
            return a_automation is not None 

    def execute(self, context):
        a_set, a_automation = return_active_set_automation(context)
        a_automation.key_assignment = self._event

        self.report({'INFO'}, "%s Assigned" % self._event)

        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in event_list.used_event and event.value == "PRESS":
            self._event = event.type
            self.execute(context)
            return {'FINISHED'}

        elif event.type in event_list.shortcut_event or event.type in event_list.passthrough_event:
            if event.value == "PRESS":
                if event.type in {"LEFTMOUSE", "RIGHTMOUSE", "ESC"}:
                    self.cancel(context)
                    return {'CANCELLED'}
                else:
                    self.report({"INFO"}, "Unavailable key")

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        # check for 3d viewport context
        if context.space_data.type != "VIEW_3D":
            self.report({"WARNING"}, "Active space must be a View3d")
            return {"CANCELLED"}

        # draw
        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_key_assign_helper_callback_px, args, 'WINDOW', 'POST_PIXEL')
        
        # modal
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        self.report({'INFO'}, "Cancelled, no key assigned")


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Assign_Key)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Assign_Key)