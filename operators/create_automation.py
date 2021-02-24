import bpy


def automation_set_callback(scene, context):

    items = [
        ('CREATE_NEW', "Create New", ""),
    ]

    scn = context.scene
    for a_s in scn.pupt_properties.automation_set:
         items.append((a_s.name, a_s.name, ""))

    return items


class PUPT_OT_Create_Automation(bpy.types.Operator):
    bl_idname = "pupt.create_automation"
    bl_label = "Create automation"
    bl_options = {"REGISTER", "UNDO"} #, "INTERNAL"}
    bl_description = "Create puppeteer automation"

    automation_set : bpy.props.EnumProperty(
        name = "Automation Set",
        items = automation_set_callback,
        )

    new_automation_set_name : bpy.props.StringProperty(name = "Set name", default = "New set")

    automation_name : bpy.props.StringProperty(name = "Automation name", default = "New automation")

    @classmethod
    def poll(cls, context):
        return True
 
    def invoke(self, context, event):
        pupt_props = context.scene.pupt_properties
        idx = pupt_props.automation_set_index
        sets = pupt_props.automation_set

        if idx in range(0,len(sets)):
            self.automation_set = context.scene.pupt_properties.automation_set[pupt_props.automation_set_index].name

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        self.layout.prop(self, "automation_set")

        if self.automation_set == "CREATE_NEW":
            self.layout.prop(self, "new_automation_set_name")

        self.layout.prop(self, "automation_name")
        
    def execute(self, context):

        pupt_props = context.scene.pupt_properties
        automation_sets = pupt_props.automation_set

        #refresh ui
        for area in context.screen.areas:
            area.tag_redraw()

        self.report({'INFO'}, "Automation created")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Create_Automation)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Create_Automation)