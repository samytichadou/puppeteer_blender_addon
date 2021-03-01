action = bpy.data.actions["action_id"]
for fcu in action.fcurves:
    print(fcu.data_path + " channel " + str(fcu.array_index))
    for keyframe in fcu.keyframe_points:
        print(keyframe.co) #coordinates x,y
        print(keyframe.select_control_point) #selected or not

        
# from dopesheet or graph ed
for fc in context.visible_fcurves:
    print("curve data_path " + fc.data_path)
    print("curve array_index " + str(fc.array_index))
    for kf in fc.keyframe_points:
        if kf.select_control_point:
            print()
            print("frame " + str(kf.co[0]))
            print("value " + str(kf.co[1]))
            print()


object.animation_data.action.fcurves[0].keyframe_points[0].co[0]

context.active_editable_fcurve
context.editable_fcurves
context.selected_visible_fcurves


-> scene
    # assignment
    -> automation name
    -> key assignment
    -> automation datas
        #key
        -> object name
        -> object type
        -> fcurve data_path
        -> fcurve array_index
        -> fcurve co
    -> 


# modal shortcut
space = play
shift = Additive

# modal infos
active keying set
show help

if help:
    special shortcuts
    automations