import bpy

class PUPT_UL_automation_set(bpy.types.UIList): 

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.prop(item, "name", text="", emboss=False)
            
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.prop(item, "name", text="", emboss=False)


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_UL_automation_set)

def unregister():
    bpy.utils.unregister_class(PUPT_UL_automation_set)
