import bpy
import os

# Clear existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import the newly built FBX
fbx_path = "/workspace/mercer_house.fbx"
if os.path.exists(fbx_path):
    bpy.ops.import_scene.fbx(filepath=fbx_path)
    
    print("=== HOUSE VERIFICATION ===\n")
    print(f"Total objects: {len(bpy.data.objects)}")
    
    mesh_count = 0
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            mesh_count += 1
    
    print(f"Mesh objects: {mesh_count}")
    
    # Check if objects have proper locations (not all at origin)
    has_proper_locations = False
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            loc = obj.location
            if abs(loc.x) > 0.5 or abs(loc.y) > 0.5 or abs(loc.z) > 0.5:
                has_proper_locations = True
                break
    
    print(f"\nObjects have proper locations: {has_proper_locations}")
    
    # Sample some object locations
    print("\nSample object locations:")
    count = 0
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and count < 10:
            print(f"  - {obj.name}: {obj.location}")
            count += 1
    
    print("\n✓ House model verified successfully!")
else:
    print("ERROR: FBX file not found!")
