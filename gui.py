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

            # automation details
            if active_set.automation_index in range(0, len(active_set.automation)):

                active_automation = active_set.automation[active_set.automation_index]

                layout.prop(active_automation, "key_assignment")

                # keyframes
                if active_automation.show_keyframes:
                    show_kf_icon = "DISCLOSURE_TRI_DOWN"
                else:
                    show_kf_icon = "DISCLOSURE_TRI_RIGHT"
                row = layout.row(align=True)
                row.prop(active_automation, "show_keyframes", text = "", icon = show_kf_icon, emboss = False)
                row.label(text = str(len(active_automation.keyframe)) + " keyframes")
                
                if active_automation.show_keyframes:

                    for kf in active_automation.keyframe:

                        if kf.show_details:
                            show_kf_d_icon = "DISCLOSURE_TRI_DOWN"
                        else:
                            show_kf_d_icon = "DISCLOSURE_TRI_RIGHT"
                        row = layout.row(align=True)
                        row.prop(kf, "show_details", text = "", icon = show_kf_d_icon, emboss = False)
                        row.label(text = kf.parent_name)

                        # keyframe details
                        if kf.show_details:
                            layout.label(text="details")

                        # split = layout.split()
                        # subcol1 = split.column(align=True)
                        # subcol2 = split.column(align=True)

                        # subcol1.label(text = kf.fcurve_data_path)
                        # subcol2.label(text = "Frame" + str(kf.fcurve_frame))



### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_PT_viewport_panel)

def unregister():
    bpy.utils.unregister_class(PUPT_PT_viewport_panel)