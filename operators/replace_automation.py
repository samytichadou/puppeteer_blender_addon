import bpy

from ..properties import key_assignment_callback
from ..gui import return_active_set_automation
from .automation_set_actions import add_item_to_collection

from . import create_automation


# enum callback for automation set
def automation_set_callback(scene, context):

    items = []

    scn = context.scene
    for a_s in scn.pupt_properties.automation_set:
         items.append((a_s.name, a_s.name, ""))

    return items


# enum callback for automation set
def automation_callback(scene, context):
    
    items = []

    a_s = context.scene.pupt_properties.automation_set[scene.automation_set]
    for a in a_s.automation:
         items.append((a.name, a.name, ""))

    return items


class PUPT_OT_Replace_Automation(bpy.types.Operator):
    bl_idname = "pupt.replace_automation"
    bl_label = "Replace automation"
    bl_options = {"REGISTER", "UNDO"} #, "INTERNAL"}
    bl_description = "Replace puppeteer existing automation"

    automation_set : bpy.props.EnumProperty(
        name = "Automation Set",
        items = automation_set_callback,
        )
    automation : bpy.props.EnumProperty(
        name = "Automation",
        items = automation_callback,
        )
    key_assignment : bpy.props.EnumProperty(
        name = "Key Assignment",
        items = key_assignment_callback,
        )

    @classmethod
    def poll(cls, context):
        if context.visible_fcurves:
            for fc in context.visible_fcurves:
                if create_automation.return_selected_keyframes(fc):
                    props = context.scene.pupt_properties
                    if props.automation_set:
                        for a_set in props.automation_set:
                            if a_set.automation:
                                return True
 
    def invoke(self, context, event):
        a_set, a_automation = return_active_set_automation(context)

        if a_set is not None:
            self.automation_set = a_set.name

        if a_automation is not None:
            self.automation = a_automation.name
            self.key_assignment = a_automation.key_assignment

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "automation_set", text = "Set")
        layout.prop(self, "automation", text = "Automation")
        layout.prop(self, "key_assignment", text = "Key")
        layout.label(text = "This will overwrite selected Automation", icon = "ERROR")
        
    def execute(self, context):
        pupt_props = context.scene.pupt_properties
        a_set = pupt_props.automation_set[self.automation_set]
        a_automation = a_set.automation[self.automation]

        # store old keyframes
        old_kf = []
        for k in a_automation.keyframe:
            old_kf.append(k.name)

        # get keyframes in collection
        if create_automation.add_keyframes_to_collection(context, a_automation):
            # remove old keyframes
            for k in old_kf:
                a_automation.keyframe.remove(a_automation.keyframe.find(k))
            a_automation.key_assignment = self.key_assignment
            a_automation.keyframe_index = 0
            self.report({'INFO'}, "Automation replaced")

        else:
            # remove created automation
            self.report({'INFO'}, "No Valid Keyframes")

        # refresh ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Replace_Automation)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Replace_Automation)