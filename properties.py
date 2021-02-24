import bpy


class PUPT_PR_automation_keyframe(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''

    object_name : bpy.props.StringProperty(name = "Object Name")
    object_type : bpy.props.StringProperty(name = "Object Type")

    fcurve_data_path : bpy.props.StringProperty(name = "Fcurve Data Path")
    fcurve_array_index : bpy.props.IntProperty(name = "Fcurve Array Index")

    fcurve_frame : bpy.props.IntProperty(name = "Fcurve Frame")
    fcurve_value : bpy.props.FloatProperty(name = "Fcurve Value")
    fcurve_additive_value : bpy.props.FloatProperty(name = "Fcurve Additive Value")


class PUPT_PR_automation(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''

    key_assignment : bpy.props.StringProperty(name = "Key")

    automation_keyframes : bpy.props.CollectionProperty(
        name = "Keyframes",
        type = PUPT_PR_automation_keyframe,
        )


class PUPT_PR_automation_set(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''

    automation : bpy.props.CollectionProperty(type = PUPT_PR_automation, name="Automation")
    automation_index : bpy.props.IntProperty(name = "Automation Index")


class PUPT_PR_properties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''

    automation_set : bpy.props.CollectionProperty(type = PUPT_PR_automation_set, name="Automation Set")
    automation_set_index : bpy.props.IntProperty(name = "Automation Set Index")


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_PR_automation_keyframe)
    bpy.utils.register_class(PUPT_PR_automation)
    bpy.utils.register_class(PUPT_PR_automation_set)
    bpy.utils.register_class(PUPT_PR_properties)

    bpy.types.Scene.pupt_properties = \
        bpy.props.PointerProperty(type = PUPT_PR_properties, name="Puppeteer Properties")

def unregister():
    bpy.utils.unregister_class(PUPT_PR_automation_keyframe)
    bpy.utils.unregister_class(PUPT_PR_automation)
    bpy.utils.unregister_class(PUPT_PR_automation_set)
    bpy.utils.unregister_class(PUPT_PR_properties)

    del bpy.types.Scene.pupt_properties