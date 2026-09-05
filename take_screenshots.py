import bpy
import os

# Ensure output directory exists
output_dir = "/workspace/screenshots"
os.makedirs(output_dir, exist_ok=True)

# Set render settings - use WORKSPACE for headless rendering without GPU
scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.engine = 'BLENDER_EEVEE'
scene.render.image_settings.file_format = 'PNG'

# Force software rendering / disable GPU requirements
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'NONE'

# Import the FBX file
fbx_path = "/workspace/mercer_house.fbx"
print(f"Importing {fbx_path}...")
bpy.ops.import_scene.fbx(filepath=fbx_path)
print("Import complete.")

# Setup a basic light since EEVEE needs lighting
if "Sun" not in bpy.data.objects:
    sun_data = bpy.data.lights.new("Sun", type='SUN')
    sun_obj = bpy.data.objects.new("Sun", sun_data)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (0.5, 0.3, 0.8)
    sun_data.energy = 2.0

# Helper function to setup camera and render
def take_snapshot(name, location, rotation, focal_length=35):
    # Create or get camera
    if "SnapshotCamera" not in bpy.data.cameras:
        cam_data = bpy.data.cameras.new("SnapshotCamera")
        cam_obj = bpy.data.objects.new("SnapshotCamera", cam_data)
        bpy.context.collection.objects.link(cam_obj)
    else:
        cam_obj = bpy.data.objects["SnapshotCamera"]
    
    cam = cam_obj.data
    cam.lens = focal_length
    
    # Position camera
    cam_obj.location = location
    cam_obj.rotation_euler = rotation
    
    # Set as active camera
    scene.camera = cam_obj
    
    # Set output path
    scene.render.filepath = os.path.join(output_dir, f"{name}.png")
    
    # Render
    print(f"Rendering {name} from {location}...")
    try:
        bpy.ops.render.render(write_still=True)
        print(f"Saved {name}.png")
    except Exception as e:
        print(f"Failed to render {name}: {e}")

# Define views for each room based on the house layout
views = [
    ("01_Exterior_Front", (15, -15, 8), (1.15, 0, 0.8)), 
    ("02_Exterior_Side", (-15, 0, 8), (1.4, 0, -0.2)),
    ("03_Living_Room", (4, -6, 2.5), (1.35, 0, -0.2)),
    ("04_Kitchen", (4, 6, 2.5), (1.35, 0, 0.2)),
    ("05_Hallway_Ground", (0, 0, 2.5), (1.35, 0, 0)),
    ("06_Stairs", (0, -2, 1.5), (1.2, 0, 0.5)),
    ("07_Leos_Bedroom", (4, -6, 6.5), (1.35, 0, -0.2)),
    ("08_Parents_Bedroom", (4, 6, 6.5), (1.35, 0, 0.2)),
    ("09_Bathroom", (-3, 4, 6.5), (1.35, 0, 0.5)),
    ("10_Basement", (0, 0, 0.5), (1.45, 0, 0)),
]

for name, loc, rot in views:
    take_snapshot(name, loc, rot)

print("All screenshots completed.")
