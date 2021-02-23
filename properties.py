import bpy


class PUPT_PR_automation_keyframe(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''

    object_name : bpy.props.StringProperty(name = "Object Name")
    object_type : bpy.props.StringProperty(name = "Object Type")

    fcurve_data_path : bpy.props.StringProperty(name = "Fcurve Data Path")
    fcurve_array_index : bpy.props.IntProperty(name = "Fcurve Array Index")

    fcurve_co : bpy.props.FloatVectorProperty(name = "Fcurve Co", size = 2)


class PUPT_PR_automation(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''

    key_assignment : bpy.props.StringProperty(name = "Key")

    automation_keyframes : bpy.props.CollectionProperty(
        name = "Keyframes",
        type = PUPT_PR_automation_keyframe,
        )


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_PR_automation_keyframe)
    bpy.utils.register_class(PUPT_PR_automation)

    bpy.types.Scene.pupt_automation = \
        bpy.props.CollectionProperty(type = PUPT_PR_automation, name="Puppeteer Automation")

def unregister():
    bpy.utils.unregister_class(PUPT_PR_automation_keyframe)
    bpy.utils.unregister_class(PUPT_PR_automation)

    del bpy.types.Scene.pupt_automation