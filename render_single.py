import bpy
import os

output_dir = "/workspace/screenshots"
os.makedirs(output_dir, exist_ok=True)

scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.engine = 'BLENDER_EEVEE'
scene.render.image_settings.file_format = 'PNG'

# Import FBX
fbx_path = "/workspace/mercer_house.fbx"
print(f"Importing {fbx_path}...")
bpy.ops.import_scene.fbx(filepath=fbx_path)
print("Import complete.")

# Add light if needed
if "Sun" not in bpy.data.objects:
    sun_data = bpy.data.lights.new("Sun", type='SUN')
    sun_obj = bpy.data.objects.new("Sun", sun_data)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (0.5, 0.3, 0.8)
    sun_data.energy = 2.0

def take_snapshot(name, location, rotation, focal_length=35):
    if "SnapshotCamera" not in bpy.data.cameras:
        cam_data = bpy.data.cameras.new("SnapshotCamera")
        cam_obj = bpy.data.objects.new("SnapshotCamera", cam_data)
        bpy.context.collection.objects.link(cam_obj)
    else:
        cam_obj = bpy.data.objects["SnapshotCamera"]
    
    cam = cam_obj.data
    cam.lens = focal_length
    cam_obj.location = location
    cam_obj.rotation_euler = rotation
    scene.camera = cam_obj
    scene.render.filepath = os.path.join(output_dir, f"{name}.png")
    
    print(f"Rendering {name}...")
    bpy.ops.render.render(write_still=True)
    print(f"Saved {name}.png")

# Render missing stairs view
take_snapshot("06_Stairs", (0, -2, 1.5), (1.2, 0, 0.5))
print("Done!")
