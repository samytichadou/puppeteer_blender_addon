import bpy
import os

from .gui import draw_update_needed_warning

addon_name = os.path.basename(os.path.dirname(__file__))


class PUPT_PF_Addon_Prefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    ui_text_color : bpy.props.FloatVectorProperty(
            name = "UI Text Color", 
            size = 4,
            min = 0.0,
            max = 1.0,
            default = [1, 1, 1, 1],
            subtype = 'COLOR'
            )

    ui_text_size : bpy.props.IntProperty(
            name = "UI Text Size",
            default = 14,
            min = 6,
            max = 99,
            )

    hold_additive : bpy.props.BoolProperty(
            name = "Hold Additive",
            description = "Hold Alt to active Additive Mode instead of toggling it"
        )

    debug : bpy.props.BoolProperty(
            name = "Debug",
            description = "Add some debug print statement in the console",
        )

    def draw(self, context):
        layout = self.layout

        # update warning
        draw_update_needed_warning(layout, context.scene.pupt_properties)

        layout.operator("pupt.check_new_version")

        row = layout.row(align = True)
        row.label(text = "UI Text")
        row.prop(self, "ui_text_color", text = "")
        row.prop(self, "ui_text_size", text = "Size")

        layout.prop(self, "hold_additive", text = "Hold Shift for Additive mode")

        layout.prop(self, "debug")
 

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_PF_Addon_Prefs)

def unregister():
    bpy.utils.unregister_class(PUPT_PF_Addon_Prefs)