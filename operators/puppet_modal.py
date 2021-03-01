import bpy
import blf


from .. import event_list
from ..addon_prefs import get_addon_preferences
from ..gui import return_active_set_automation


def draw_callback_px(self, context):
    font_id = 0  # XXX, need to find out how best to get this.
    
    prefs = get_addon_preferences()
    col = prefs.ui_text_color
    size = prefs.ui_text_size

    a_set, a_automation = return_active_set_automation(context)
    if a_set is None:
        name = "None"
    else:
        name = a_set.name

    # draw some text
    blf.color(0, *col)
    blf.position(font_id, 15, 30, 0)
    blf.size(font_id, size, 72)
    blf.draw(font_id, "Puppet Set : " + name)


class PUPT_OT_Puppet_Modal(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "pupt.puppet_modal"
    bl_label = "Puppet"

    _modifier_shift = False


    @classmethod
    def poll(cls, context):
        if len(context.scene.pupt_properties.automation_set) != 0:
            return True


    def modal(self, context, event):
        context.area.tag_redraw()
        
        # special shortcuts
        if event.type in event_list.shortcut_event:
            # ESC
            if event.type == 'ESC':
                print("finished " + event.value)
                self.finish(context)
                return {'FINISHED'}
            # SPACE
            elif event.type == 'SPACE' and event.value == "PRESS":
                print("space " + event.value)
                if not context.screen.is_animation_playing:
                    bpy.ops.screen.animation_play()
                else:
                    bpy.ops.screen.animation_cancel(restore_frame = False)  

        # action
        elif event.type in event_list.used_event and event.value == "PRESS":
            if self._modifier_shift:
                print("modifier shift")
            print(event.type)
            print("other " + event.value)

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
        #return {'PASS_THROUGH'}


    def invoke(self, context, event):
        # check for 3d viewport context
        if context.space_data.type != "VIEW_3D":
            self.report({"WARNING"}, "Active space must be a View3d")
            return {"CANCELLED"}

        # draw
        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

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