import bpy


from ..version_check import check_addon_version


class PUPT_OT_Check_New_Version(bpy.types.Operator):
    bl_idname = "pupt.check_new_version"
    bl_label = "Check for new version"
    bl_description = "Check online for new version of the addon"

    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):
        
        if check_addon_version():
            if context.scene.pupt_properties.update_needed:
                self.report({'INFO'}, "New version found")
            else:
                self.report({'INFO'}, "No new version")
        else:
            self.report({'INFO'}, "No internet connection")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Check_New_Version)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Check_New_Version)