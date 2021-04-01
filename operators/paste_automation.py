import bpy

from ..gui  import return_active_set_automation
from .puppet_modal import set_keyframe_from_paste_mode


class PUPT_OT_Paste_Automation(bpy.types.Operator):
    bl_idname = "pupt.paste_automation"
    bl_label = "Paste Automation"
    bl_options = {"UNDO", "INTERNAL"}
    bl_description = "Paste Selected Automation"

    @classmethod
    def poll(cls, context):
        a_set, a_automation = return_active_set_automation(context)
        return a_automation is not None
        
    def execute(self, context):
        props = context.scene.pupt_properties
        a_set, a_automation = return_active_set_automation(context)
        current_frame = context.scene.frame_current

        for kf in a_automation.keyframe:
            chk_paste = set_keyframe_from_paste_mode(kf, current_frame, props.additive_keyframing, props.paste_mode)

            if not chk_paste:
                print("Puppeteer --- Unable to paste keyframe")

        for area in context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "%s Automation Applied" % a_automation.name)

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Paste_Automation)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Paste_Automation)