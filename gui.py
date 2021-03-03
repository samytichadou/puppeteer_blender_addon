import bpy



def return_active_set_automation(context):

    active_set = active_automation = None

    props = context.scene.pupt_properties

    if props.automation_set_index in range(0, len(props.automation_set)):
        active_set = props.automation_set[props.automation_set_index]
        if active_set.automation_index in range(0, len(active_set.automation)):
            active_automation = active_set.automation[active_set.automation_index]
            
    return active_set, active_automation



# main panel
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

        layout.operator("pupt.puppet_modal")
        layout.prop(props, "paste_mode")

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


# keyframe subpanel
class PUPT_PT_viewport_keyframes_subpanel(bpy.types.Panel):
    bl_label = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "PUPT_PT_viewport_panel"
    bl_options = {'DEFAULT_CLOSED'}
 
    @classmethod
    def poll(cls, context):
        a_set, a_automation = return_active_set_automation(context)
        if a_automation is not None:
            if a_automation.keyframe:
                return True

    def draw_header(self, context):
        a_set, a_automation = return_active_set_automation(context)
        self.layout.label(text = "%i Keyframes" % len(a_automation.keyframe))
 
    def draw(self, context):

        layout = self.layout

        a_set, a_automation = return_active_set_automation(context)

        layout.template_list("PUPT_UL_keyframes", "", a_automation, "keyframe", a_automation, "keyframe_index", rows = 2)

        # keyframe details
        if a_automation.keyframe_index in range(0, len(a_automation.keyframe)):
            a_kf = a_automation.keyframe[a_automation.keyframe_index]

            split = layout.split()

            col1 = split.column(align=True)
            col2 = split.column(align=True)
            
            col1.label(text = "Parent :")
            col2.label(text = a_kf.parent_name)

            col1.label(text = "Type :")
            col2.label(text = a_kf.parent_type)

            col1.label(text = "Action :")
            col2.label(text = a_kf.action_name)

            if "_NTREE" in a_kf.parent_type:
                col1.label(text = "Node :")
                col2.label(text = a_kf.node_name)

                col1.label(text = "Socket :")
                col2.label(text = a_kf.socket_type + "[%i]" % a_kf.socket_index)

            elif "_POSE" in a_kf.parent_type:
                col1.label(text = "Bone :")
                col2.label(text = a_kf.bone_name)

            col1.label(text = "FCurve :")
            col2.label(text = a_kf.fcurve_data_path + "[%i]" % a_kf.fcurve_array_index)

            col1.label(text = "Frame :")
            col2.label(text = str(a_kf.fcurve_frame))

            col1.label(text = "Value :")
            col2.label(text = str(a_kf.fcurve_value))

            col1.label(text = "Additive Value :")
            col2.label(text = str(a_kf.fcurve_additive_value))


# key menu entry for creating automation
def draw_dopesheet_key_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("pupt.create_automation")
        

### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_PT_viewport_panel)
    bpy.utils.register_class(PUPT_PT_viewport_keyframes_subpanel)
    bpy.types.DOPESHEET_MT_key.append(draw_dopesheet_key_menu)

def unregister():
    bpy.utils.unregister_class(PUPT_PT_viewport_panel)
    bpy.utils.unregister_class(PUPT_PT_viewport_keyframes_subpanel)
    bpy.types.DOPESHEET_MT_key.remove(draw_dopesheet_key_menu)