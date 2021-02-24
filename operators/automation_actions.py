import bpy


class PUPT_OT_Automation_Actions(bpy.types.Operator):
    bl_idname = "pupt.automation_actions"
    bl_label = "Automation actions"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}
    bl_description = "Puppeteer automation actions"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            )
        )

    @classmethod
    def poll(cls, context):
        pupt_props = context.scene.pupt_properties
        if pupt_props.automation_set_index in range(0,len(pupt_props.automation_set)):
            active_set = pupt_props.automation_set[pupt_props.automation_set_index]
            return active_set.automation_index in range(0, len(active_set.automation))
        
    def execute(self, context):
        
        pupt_props = context.scene.pupt_properties
        active_set = pupt_props.automation_set[pupt_props.automation_set_index]
        automations = active_set.automation
        idx = active_set.automation_index

        # remove
        if self.action == 'REMOVE':
            automations.remove(idx)

            if idx != 0:
                active_set.automation_index -= 1
            
            self.report({'INFO'}, "Automation removed")

        # down
        elif self.action == 'DOWN':
            if idx < len(automations) - 1:
                automations.move(idx, idx+1)
                active_set.automation_index += 1

                self.report({'INFO'}, "Automation moved")
            else:
                self.report({'INFO'}, "Unable to move in this direction")

        # up
        elif self.action == 'UP':
            if idx >= 1:
                automations.move(idx, idx-1)
                active_set.automation_index -= 1

                self.report({'INFO'}, "Automation moved")
            else:
                self.report({'INFO'}, "Unable to move in this direction")

        # refresh ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Automation_Actions)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Automation_Actions)