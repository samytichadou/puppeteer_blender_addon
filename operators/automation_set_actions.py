import bpy


#add item to collection property
def add_item_to_collection(collection, base_name):

    #check for dupes
    old_names = []
    for i in collection:
        if base_name in i.name:
            old_names.append(i.name)
    
    count = 0
    new_name = base_name
    while new_name in old_names:
        new_name = base_name + "_" + str(count).zfill(3)
        count += 1

    #add
    new_set = collection.add()
    new_set.name = new_name
    

class PUPT_OT_Automation_Set_Actions(bpy.types.Operator):
    bl_idname = "pupt.automation_set_actions"
    bl_label = "Set actions"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}
    bl_description = "Puppeteer automation set actions"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", ""),
            ('ADD', "Add", "")))

    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):

        pupt_props = context.scene.pupt_properties
        sets = pupt_props.automation_set
        idx = pupt_props.automation_set_index

        # add
        if self.action == "ADD":
            add_item_to_collection(sets, "new_set")

            pupt_props.automation_set_index = len(sets) - 1

            self.report({'INFO'}, "Automation set created")

        elif idx in range(0,len(sets)):

            # remove
            if self.action == 'REMOVE':
                sets.remove(idx)

                if idx != 0:
                    pupt_props.automation_set_index -= 1
                
                self.report({'INFO'}, "Automation set removed")

            # down
            elif self.action == 'DOWN':
                if idx < len(sets) - 1:
                    sets.move(idx, idx+1)
                    pupt_props.automation_set_index += 1

                    self.report({'INFO'}, "Automation set moved")
                else:
                    self.report({'INFO'}, "Unable to move in this direction")

            # up
            elif self.action == 'UP':
                if idx >= 1:
                    sets.move(idx, idx-1)
                    pupt_props.automation_set_index -= 1

                    self.report({'INFO'}, "Automation set moved")
                else:
                    self.report({'INFO'}, "Unable to move in this direction")

        else:
            self.report({'INFO'}, "No set selected")
            return {'FINISHED'}

        # refresh ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Automation_Set_Actions)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Automation_Set_Actions)