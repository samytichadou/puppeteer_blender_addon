action = bpy.data.actions["action_id"]
for fcu in action.fcurves:
    print(fcu.data_path + " channel " + str(fcu.array_index))
    for keyframe in fcu.keyframe_points:
        print(keyframe.co) #coordinates x,y


object.animation_data.action.fcurves[0].keyframe_points[0].co[0]