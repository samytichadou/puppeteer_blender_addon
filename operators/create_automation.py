import bpy


from .automation_set_actions import add_item_to_collection
from ..properties import key_assignment_callback


# enum callback for automation set
def automation_set_callback(scene, context):

    items = [
        ('CREATE_NEW', "Create New", ""),
    ]

    scn = context.scene
    for a_s in scn.pupt_properties.automation_set:
         items.append((a_s.name, a_s.name, ""))

    return items


# return keyframes
def return_selected_keyframes(fcurve):

    keyframes = []

    for kf in fcurve.keyframe_points:
        if kf.select_control_point:
            keyframes.append(kf)

    return sorted(keyframes, key=lambda x: x.co[0])


# get first keyframe in time out of a list
def get_init_keyframe(keyframe_list):
    
    original_frame = min(keyframe_list, key=lambda item: item.co[0])

    return original_frame


# return action/parent list
def return_parent_action(context, fcurve):

    action = fcurve.id_data

    # objects
    for ob in context.scene.objects:
        if ob.animation_data:
            if action == ob.animation_data.action:
                if "pose.bones" in fcurve.data_path:
                    return ob, "OBJECT_POSE"
                else:
                    return ob, "OBJECT"

    # materials and nodetree
    for ma in bpy.data.materials:
        # materials
        if ma.animation_data:
            if action == ma.animation_data.action:
                return ma, "MATERIAL"
        # nodetree
        if not ma.is_grease_pencil:
            if ma.node_tree.animation_data:
                if action == ma.node_tree.animation_data.action:
                    return ma, "MATERIAL_NTREE"

    # worlds and nodetree
    for wo in bpy.data.worlds:
        # worlds
        if wo.animation_data:
            if action == wo.animation_data.action:
                return wo, "WORLD"
        # nodetree
        if wo.node_tree.animation_data:
            if action == wo.node_tree.animation_data.action:
                return wo, "WORLD_NTREE"

    return None, None


# split nodes data path and format it
def split_nodes_data_path(long_data_path):

    node_name = long_data_path.split('nodes["')[1].split('"]')[0]

    shorten = long_data_path.split('"].')[1]

    socket = shorten.split('[')[0]
    socket_index = shorten.split('[')[1].split(']')[0]

    data_path = shorten.split('].')[1]

    return node_name, socket, socket_index, data_path


# split pose data path and format it 
def split_pose_data_path(long_data_path):

    shorten = long_data_path.split("pose.")[1]

    bone_name = shorten.split('["')[1].split('"].')[0]

    data_path = shorten.split('].')[1]

    return bone_name, data_path


# keyframe infos
def add_keyframes_to_collection(context, collection):

    fc_keyframes = []
    frames = []
    automation_check = False

    for fc in context.visible_fcurves:

        fc_keyframes.clear()       
        fc_keyframes = return_selected_keyframes(fc)

        # ignore fcurve if no selected keyframes
        if not fc_keyframes:
            continue

        #get initial frame/value
        init_keyframe = get_init_keyframe(fc_keyframes)
        frames.append(init_keyframe.co[0])
        init_value = init_keyframe.co[1]

        # get parent action
        parent_action, parent_type = return_parent_action(context, fc)

        # ignore fcurve if undetailed parent type (NodeGroups)
        if parent_type is None:
            continue

        automation_check = True

        if "_NTREE" in parent_type:
            node_infos = split_nodes_data_path(fc.data_path)
            #[0]node_name, [1]socket, [2]socket_index, [3]data_path
            data_path = node_infos[3]
        elif "_POSE" in parent_type:
            pose_infos = split_pose_data_path(fc.data_path)
            #[0]bone_name, [1]data_path
            data_path = pose_infos[1]
        else:
            data_path = fc.data_path

        for kf in fc_keyframes:

            new_key = collection.keyframe.add()

            if parent_action is not None:
                new_key.parent_name = parent_action.name
                new_key.parent_type = parent_type
            new_key.parent_subtype = fc.id_data.id_root

            new_key.action_name = fc.id_data.name

            new_key.fcurve_data_path = data_path
            new_key.fcurve_array_index = fc.array_index

            new_key.fcurve_frame = kf.co[0]
            new_key.fcurve_value = kf.co[1]
            new_key.fcurve_additive_value = kf.co[1] - init_value

            if "_NTREE" in parent_type:
                new_key.node_name = node_infos[0]
                new_key.socket_type = node_infos[1].upper()
                new_key.socket_index = int(node_infos[2])

            elif "_POSE" in parent_type:
                new_key.bone_name = pose_infos[0]

    
    # set relative frames
    if frames:
        origin_frame = min(frames)
        
        for kf in collection.keyframe:
            kf.fcurve_frame = kf.fcurve_frame - origin_frame

    return automation_check
          

class PUPT_OT_Create_Automation(bpy.types.Operator):
    bl_idname = "pupt.create_automation"
    bl_label = "Create automation"
    bl_options = {"REGISTER", "UNDO"} #, "INTERNAL"}
    bl_description = "Create puppeteer automation"

    automation_set : bpy.props.EnumProperty(
        name = "Automation Set",
        items = automation_set_callback,
        )
    new_automation_set_name : bpy.props.StringProperty(name = "Set name", default = "new_set")
    automation_name : bpy.props.StringProperty(name = "Automation name", default = "new_automation")
    key_assignment : bpy.props.EnumProperty(
        name = "Key Assignment",
        items = key_assignment_callback,
        )

    @classmethod
    def poll(cls, context):
        for fc in context.visible_fcurves:
            if return_selected_keyframes(fc):
                return True
 
    def invoke(self, context, event):
        pupt_props = context.scene.pupt_properties
        idx = pupt_props.automation_set_index
        sets = pupt_props.automation_set

        if idx in range(0,len(sets)):
            self.automation_set = context.scene.pupt_properties.automation_set[pupt_props.automation_set_index].name

        return context.window_manager.invoke_props_dialog(self)
 
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "automation_set")

        if self.automation_set == "CREATE_NEW":
            layout.prop(self, "new_automation_set_name")

        layout.prop(self, "automation_name")
        layout.prop(self, "key_assignment")
        
    def execute(self, context):

        pupt_props = context.scene.pupt_properties
        sets = pupt_props.automation_set

        # create new set if needed
        if self.automation_set == "CREATE_NEW":
            add_item_to_collection(sets, self.new_automation_set_name)
            
            pupt_props.automation_set_index = len(sets) - 1

            active_set = sets[pupt_props.automation_set_index]

        else:
            active_set = sets[self.automation_set]

        # create automation
        new_automation = add_item_to_collection(active_set.automation, self.automation_name)

        # get keyframes in collection
        if add_keyframes_to_collection(context, new_automation):

            new_automation.key_assignment = self.key_assignment
            active_set.automation_index = len(active_set.automation)-1
            self.report({'INFO'}, "Automation created")

        else:
            # remove created automation
            active_set.automation.remove(len(active_set.automation)-1)
            self.report({'INFO'}, "No Valid Keyframes")

        # refresh ui
        for area in context.screen.areas:
            area.tag_redraw()


        return {'FINISHED'}


### REGISTER ---

def register():
    bpy.utils.register_class(PUPT_OT_Create_Automation)

def unregister():
    bpy.utils.unregister_class(PUPT_OT_Create_Automation)