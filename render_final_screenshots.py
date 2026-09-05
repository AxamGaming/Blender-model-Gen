import bpy
import os

# Import the house
bpy.ops.import_scene.fbx(filepath='/workspace/mercer_house_final.fbx')

# List all objects to debug
print("Objects in scene after import:")
for obj in bpy.data.objects:
    print(f"  - {obj.name} (type: {obj.type})")

# Delete default cube if exists
if 'Cube' in bpy.data.objects:
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()
    print("Deleted Cube")

# Get the house object - should be Mercer_House
house = bpy.data.objects.get('Mercer_House')

if not house:
    # Try to find any mesh object
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            house = obj
            print(f"Found alternative mesh: {obj.name}")
            break

if not house:
    print("Error: No mesh object found!")
    print("Available objects:", [o.name for o in bpy.data.objects])
    exit()

print(f"Using house object: {house.name}")

# Set up camera
camera_data = bpy.data.cameras.new(name='Camera')
camera_obj = bpy.data.objects.new('Camera', camera_data)
bpy.context.collection.objects.link(camera_obj)

# Set up light
light_data = bpy.data.lights.new(name='Sun', type='SUN')
light_data.energy = 1.5
light_obj = bpy.data.objects.new('Sun', light_data)
bpy.context.collection.objects.link(light_obj)
light_obj.rotation_euler = (0.5, 0.2, 0.3)

# Scene settings
scene = bpy.context.scene
scene.camera = camera_obj

# Render settings
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.image_settings.file_format = 'PNG'
scene.eevee.taa_render_samples = 64

def setup_camera_position(position, target):
    """Position camera to look at target"""
    camera_obj.location = position
    direction = tuple(t - p for p, t in zip(position, target))
    # Simple lookAt approximation
    import math
    yaw = math.atan2(direction[0], direction[1])
    pitch = math.atan2(direction[2], math.sqrt(direction[0]**2 + direction[1]**2))
    camera_obj.rotation_euler = (-pitch, 0, -yaw)

def render_view(name, cam_pos, look_at):
    """Render a view from given camera position looking at target"""
    setup_camera_position(cam_pos, look_at)
    scene.render.filepath = f'/workspace/screenshots_final/{name}.png'
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {name}")

# Create output directory
import os
os.makedirs('/workspace/screenshots_final', exist_ok=True)

# House dimensions (approximate from bounding box)
hx, hy, hz = 40, 80, 50  # Rough dimensions

# Render exterior views
render_view('01_Exterior_Front', 
            (0, -100, 40),  # Camera position
            (0, 0, 25))      # Look at center

render_view('02_Exterior_Side',
            (100, 0, 40),
            (0, 0, 25))

render_view('03_Exterior_Back',
            (0, 100, 40),
            (0, 0, 25))

render_view('04_Exterior_Angle',
            (70, -70, 50),
            (0, 0, 25))

# Interior views - need to move camera inside
# Living room (ground floor, left side)
render_view('05_Living_Room',
            (-15, -20, 8),
            (-15, 0, 5))

# Kitchen (ground floor, right side)
render_view('06_Kitchen',
            (15, -20, 8),
            (15, 0, 5))

# Stairs
render_view('07_Stairs',
            (5, 30, 8),
            (0, 20, 15))

# Leo's bedroom (second floor, left back)
render_view('08_Leos_Bedroom',
            (-15, -20, 22),
            (-15, -25, 18))

# Parents bedroom (second floor, right back)
render_view('09_Parents_Bedroom',
            (15, -20, 22),
            (15, -25, 18))

# Bathroom (second floor, right front)
render_view('10_Bathroom',
            (15, 20, 22),
            (15, 25, 18))

# Basement
render_view('11_Basement',
            (0, -20, -10),
            (0, 0, -10))

print("\nAll renders complete!")
