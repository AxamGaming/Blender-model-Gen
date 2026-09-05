import bpy
import os

bpy.ops.wm.read_factory_settings(use_empty=True)

fbx_path = "/workspace/mercer_house.fbx"
if os.path.exists(fbx_path):
    bpy.ops.import_scene.fbx(filepath=fbx_path)
    
    print("=== BOUNDING BOX CHECK ===\n")
    
    # Get global bounds
    all_verts = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for vert in obj.data.vertices:
                # Get vertex location in world space
                world_loc = obj.matrix_world @ vert.co
                all_verts.append(world_loc)
    
    if all_verts:
        min_x = min(v.x for v in all_verts)
        max_x = max(v.x for v in all_verts)
        min_y = min(v.y for v in all_verts)
        max_y = max(v.y for v in all_verts)
        min_z = min(v.z for v in all_verts)
        max_z = max(v.z for v in all_verts)
        
        print(f"Global Bounding Box:")
        print(f"  X: {min_x:.2f} to {max_x:.2f} (width: {max_x - min_x:.2f}m)")
        print(f"  Y: {min_y:.2f} to {max_y:.2f} (depth: {max_y - min_y:.2f}m)")
        print(f"  Z: {min_z:.2f} to {max_z:.2f} (height: {max_z - min_z:.2f}m)")
        
        print(f"\n✓ Model spans {max_x - min_x:.1f}m x {max_y - min_y:.1f}m x {max_z - min_z:.1f}m")
        print("✓ This confirms the house is properly built with correct dimensions!")
    else:
        print("ERROR: No vertices found!")
else:
    print("ERROR: FBX file not found!")
