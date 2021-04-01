import bpy

from ..gui import return_active_set_automation
from ..addon_prefs import get_addon_preferences
from .automation_set_actions import add_item_to_collection


# enum callback for automation set
def automation_set_callback(scene, context):

    items = [
        ('CREATE_NEW', "Create New", ""),
    ]

    a_set, a_automation = return_active_set_automation(context)

    scn = context.scene
    for a_s in scn.pupt_properties.automation_set:
        if a_set is not None and a_set == a_s:
            continue
        items.append((a_s.name, a_s.name, ""))

    return items


# set attributes between 2 dataset
def set_properties_from_dataset(datasetin, datasetout, avoid_list, debug):
    if debug: print("Puppeteer --- Copying from %s to %s" % (str(datasetin), str(datasetout))) #debug

    for prop in datasetin.bl_rna.properties:
        if not prop.is_readonly and not prop.identifier in avoid_list:
            try:
                setattr(datasetout, '%s' % prop.identifier, getattr(datasetin, prop.identifier))
            except (KeyError, AttributeError):
                if debug: print("Puppeteer --- Error copying %s" % prop.identifier) #debug
                pass


class PUPT_OT_Copy_Automation(bpy.types.Operator):
    bl_idname = "pupt.copy_automation"
    bl_label = "Copy Automation"
    bl_options = {"UNDO", "INTERNAL"}
    bl_description = "Copy selected automation"


    automation_set : bpy.props.EnumProperty(
        name = "Automation Set",
        items = automation_set_callback,
        )
    new_automation_set_name : bpy.props.StringProperty(name = "Set name", default = "new set")
    cut : bpy.props.BoolProperty(name = "Cut", description = "Remove original automation")


    @classmethod
    def poll(cls, context):
        a_set, a_automation = return_active_set_automation(context)
        return a_automation is not None


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
 

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "cut")

        layout.prop(self, "automation_set", text = "Set")

        if self.automation_set == "CREATE_NEW":
            layout.prop(self, "new_automation_set_name", text = "Set Name")
        

    def execute(self, context):

        debug = get_addon_preferences().debug
        
        pupt_props = context.scene.pupt_properties
        sets = pupt_props.automation_set
        a_set, a_automation = return_active_set_automation(context)

        # create new set if needed
        if self.automation_set == "CREATE_NEW":
            target_set = add_item_to_collection(sets, self.new_automation_set_name)
            if debug: print("Puppeteer --- New Set created : %s" % target_set.name)
        else:
            target_set = sets[self.automation_set]

        # create automation
        new_automation = add_item_to_collection(target_set.automation, a_automation.name)
        # copy automation props
        set_properties_from_dataset(a_automation, new_automation, ("name"), debug)
        # keyframes
        for k in a_automation.keyframe:
            new_k = new_automation.keyframe.add()
            set_properties_from_dataset(k, new_k, (), debug)
        if debug: print("Puppeteer --- Automation created : %s" % new_automation.name)

        # if cut, remove old automation
        if self.cut:
            a_set.automation.remove(a_set.automation_index)
            if a_set.automation_index != 0:
                a_set.automation_index -= 1
            if debug: print("Puppeteer --- Old automation removed")
        
        self.report({'INFO'}, "Automation copied")

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Copy_Automation)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Copy_Automation)