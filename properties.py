import bpy


from . import event_list


# key assignment callback
def key_assignment_callback(scene, context):

    items = []

    #for e in sorted(event_list.used_event, key = str):
    for e in event_list.used_event:
         items.append((e, e, ""))

    return items


class PUPT_PR_automation_keyframe(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''

    parent_name : bpy.props.StringProperty(name = "Parent Name")
    parent_type = bpy.props.EnumProperty(
        name = "Parent Type",
        items = (
            ('OBJECT', "Object", ""),
            ('MATERIAL', "Material", ""),
            ('MATERIAL_NTREE', "Material NTree", ""),
            ('WORLD', "World", ""),
            ('WORLD_NTREE', "World NTree", ""),
            ),
        )
    parent_subtype : bpy.props.StringProperty(name = "Parent Subtype")

    action_name : bpy.props.StringProperty(name = "Action Name")

    fcurve_data_path : bpy.props.StringProperty(name = "Fcurve Data Path")
    fcurve_array_index : bpy.props.IntProperty(name = "Fcurve Array Index")

    fcurve_frame : bpy.props.IntProperty(name = "Fcurve Frame")
    fcurve_value : bpy.props.FloatProperty(name = "Fcurve Value")
    fcurve_additive_value : bpy.props.FloatProperty(name = "Fcurve Additive Value")


class PUPT_PR_automation(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''

    key_assignment : bpy.props.EnumProperty(
        name = "Key",
        items = key_assignment_callback,
        )

    keyframe : bpy.props.CollectionProperty(
        name = "Keyframes",
        type = PUPT_PR_automation_keyframe,
        )

    keyframe_index : bpy.props.IntProperty(name = "Keyframe Index")


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