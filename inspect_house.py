import bpy
import os
import math

# Clear existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import the broken FBX to inspect
fbx_path = "/workspace/mercer_house.fbx"
if os.path.exists(fbx_path):
    bpy.ops.import_scene.fbx(filepath=fbx_path)
    
    # Count objects and check locations
    print(f"\nTotal objects in scene: {len(bpy.data.objects)}")
    mesh_count = 0
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            mesh_count += 1
            print(f"  - {obj.name}: location={obj.location}")
    print(f"\nTotal mesh objects: {mesh_count}")
else:
    print("FBX file not found!")
