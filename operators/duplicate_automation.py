import bpy

from ..gui import return_active_set_automation
from ..addon_prefs import get_addon_preferences
from .automation_set_actions import add_item_to_collection
from .copy_automation import set_properties_from_dataset


class PUPT_OT_Duplicate_Automation(bpy.types.Operator):
    bl_idname = "pupt.duplicate_automation"
    bl_label = "Duplicate Automation"
    bl_options = {"UNDO", "INTERNAL"}
    bl_description = "Duplicate selected automation"

    @classmethod
    def poll(cls, context):
        a_set, a_automation = return_active_set_automation(context)
        return a_automation is not None

    def execute(self, context):

        debug = get_addon_preferences().debug
        
        pupt_props = context.scene.pupt_properties
        sets = pupt_props.automation_set
        a_set, a_automation = return_active_set_automation(context)

        # create automation
        new_automation = add_item_to_collection(a_set.automation, a_automation.name)
        # copy automation props
        set_properties_from_dataset(a_automation, new_automation, ("name", "key_assignment"), debug)
        # keyframes
        for k in a_automation.keyframe:
            new_k = new_automation.keyframe.add()
            set_properties_from_dataset(k, new_k, (), debug)
        if debug: print("Puppeteer --- Automation created : %s" % new_automation.name)
        
        self.report({'INFO'}, "Automation duplicated")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Duplicate_Automation)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Duplicate_Automation)