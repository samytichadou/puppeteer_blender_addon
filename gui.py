import bpy


# panel
class PUPT_PT_viewport_panel(bpy.types.Panel):
    bl_label = "Puppeteer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Puppeteer"
 
    @classmethod
    def poll(cls, context):
        return True
 
    def draw(self, context):

        props = context.scene.pupt_properties

        layout = self.layout 

        # sets
        layout.label(text = "Automation Set")

        row = layout.row()

        row.template_list("PUPT_UL_automation_set", "", props, "automation_set", props, "automation_set_index", rows = 4)

        col = row.column(align=True)
        col.operator("pupt.automation_set_actions", icon='ADD', text="").action = 'ADD'
        col.operator("pupt.automation_set_actions", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("pupt.automation_set_actions", icon='TRIA_UP', text="").action = 'UP'
        col.operator("pupt.automation_set_actions", icon='TRIA_DOWN', text="").action = 'DOWN'

        # automations
        if props.automation_set_index in range(0, len(props.automation_set)):

            active_set = props.automation_set[props.automation_set_index]

            layout.label(text = "Automations")

            row = layout.row()

            row.template_list("PUPT_UL_automation", "", active_set, "automation", active_set, "automation_index", rows = 4)

            col = row.column(align=True)
            col.operator("pupt.automation_actions", icon='REMOVE', text="").action = 'REMOVE'
            col.separator()
            col.operator("pupt.automation_actions", icon='TRIA_UP', text="").action = 'UP'
            col.operator("pupt.automation_actions", icon='TRIA_DOWN', text="").action = 'DOWN'



### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_PT_viewport_panel)

def unregister():
    bpy.utils.unregister_class(PUPT_PT_viewport_panel)