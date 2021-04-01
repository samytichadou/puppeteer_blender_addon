import bpy


class PUPT_OT_Remove_Keyframe(bpy.types.Operator):
    bl_idname = "pupt.remove_keyframe"
    bl_label = "Remove Keyframe"
    bl_options = {"UNDO", "INTERNAL"}
    bl_description = "Remove Automation Keyframe"

    @classmethod
    def poll(cls, context):
        pupt_props = context.scene.pupt_properties
        if pupt_props.automation_set_index in range(0,len(pupt_props.automation_set)):
            active_set = pupt_props.automation_set[pupt_props.automation_set_index]
            if active_set.automation_index in range(0, len(active_set.automation)):
                active_automation = active_set.automation[active_set.automation_index]
                return active_automation.keyframe_index in range(0, len(active_automation.keyframe))
        
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