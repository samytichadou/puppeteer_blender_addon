import bpy

from ..gui import return_active_set_automation


class PUPT_OT_Remove_Keyframe(bpy.types.Operator):
    bl_idname = "pupt.remove_keyframe"
    bl_label = "Remove Keyframe"
    bl_options = {"UNDO", "INTERNAL"}
    bl_description = "Remove Automation Keyframe"

    @classmethod
    def poll(cls, context):
        a_set, a_automation = return_active_set_automation(context)
        if a_automation is not None:
            return a_automation.keyframe_index in range(0, len(a_automation.keyframe))               
        
    def execute(self, context):
        
        pupt_props = context.scene.pupt_properties
        active_set = pupt_props.automation_set[pupt_props.automation_set_index]
        active_automation = active_set.automation[active_set.automation_index]

        keyframes = active_automation.keyframe
        idx = active_automation.keyframe_index

        # remove
        keyframes.remove(idx)

        if idx != 0:
            active_automation.keyframe_index -= 1
        
        self.report({'INFO'}, "Automation removed")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Remove_Keyframe)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Remove_Keyframe)