import bpy
import math

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Materials - PSX style flat colors
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = color
    mat.specular_intensity = 0.2
    return mat

materials = {
    'wall_ext': create_material('WallExt', (0.75, 0.68, 0.6, 1.0)),
    'wall_int': create_material('WallInt', (0.85, 0.8, 0.7, 1.0)),
    'floor_wood': create_material('FloorWood', (0.45, 0.3, 0.2, 1.0)),
    'floor_tile': create_material('FloorTile', (0.35, 0.35, 0.4, 1.0)),
    'ceiling': create_material('Ceiling', (0.9, 0.9, 0.85, 1.0)),
    'door': create_material('Door', (0.4, 0.25, 0.15, 1.0)),
    'trim': create_material('Trim', (0.95, 0.95, 0.95, 1.0)),
    'roof': create_material('Roof', (0.3, 0.25, 0.2, 1.0)),
    'window_frame': create_material('WindowFrame', (0.95, 0.95, 0.95, 1.0)),
    'glass': create_material('Glass', (0.3, 0.5, 0.7, 0.4)),
    'carpet_red': create_material('CarpetRed', (0.55, 0.2, 0.2, 1.0)),
    'furniture_dark': create_material('FurnitureDark', (0.3, 0.2, 0.15, 1.0)),
    'furniture_light': create_material('FurnitureLight', (0.5, 0.4, 0.3, 1.0)),
    'metal': create_material('Metal', (0.55, 0.55, 0.6, 1.0)),
    'white': create_material('White', (0.88, 0.88, 0.88, 1.0)),
    'black': create_material('Black', (0.12, 0.12, 0.12, 1.0)),
    'skin': create_material('Skin', (0.85, 0.65, 0.55, 1.0)),
    'hair_brown': create_material('HairBrown', (0.2, 0.12, 0.08, 1.0)),
    'shirt_red': create_material('ShirtRed', (0.7, 0.15, 0.15, 1.0)),
    'bed_sheet': create_material('BedSheet', (0.92, 0.92, 0.95, 1.0)),
    'blanket': create_material('Blanket', (0.3, 0.45, 0.7, 1.0)),
    'toilet': create_material('Toilet', (0.92, 0.92, 0.92, 1.0)),
    'bathtub': create_material('Bathtub', (0.9, 0.9, 0.9, 1.0)),
}

all_meshes = []

def create_box(name, size, location, material=None):
    """Create a box with proper dimensions (size in meters)"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    # Scale to actual size (default cube is 2m, so we scale by size/2)
    obj.scale = (size[0]/2, size[1]/2, size[2]/2)
    if material:
        obj.data.materials.append(material)
    all_meshes.append(obj)
    return obj

def create_plane(name, size, location, rotation=(0, 0, 0), material=None):
    """Create a plane with proper dimensions"""
    bpy.ops.mesh.primitive_plane_add(size=1, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0]/2, size[1]/2, 1)
    if material:
        obj.data.materials.append(material)
    all_meshes.append(obj)
    return obj

# House dimensions (realistic scale in meters)
house_width = 8.0      # Width (X axis)
house_depth = 10.0     # Depth (Y axis) 
floor_height = 3.0     # Height per floor
wall_thickness = 0.15  # Wall thickness
basement_depth = 2.5   # Basement height

# === BASEMENT ===
basement_z = -basement_depth

# Basement floor
create_plane('Basement_Floor', (house_width, house_depth), 
             (0, 0, basement_z - 0.1), material=materials['floor_tile'])

# Basement walls
create_box('Basement_Wall_Back', (house_width, wall_thickness, basement_depth),
           (0, -house_depth/2 + wall_thickness/2, basement_z - basement_depth/2), 
           material=materials['wall_ext'])
create_box('Basement_Wall_Front', (house_width, wall_thickness, basement_depth),
           (0, house_depth/2 - wall_thickness/2, basement_z - basement_depth/2),
           material=materials['wall_ext'])
create_box('Basement_Wall_Left', (wall_thickness, house_depth, basement_depth),
           (-house_width/2 + wall_thickness/2, 0, basement_z - basement_depth/2),
           material=materials['wall_ext'])
create_box('Basement_Wall_Right', (wall_thickness, house_depth, basement_depth),
           (house_width/2 - wall_thickness/2, 0, basement_z - basement_depth/2),
           material=materials['wall_ext'])

# Basement stairs going down
for i in range(8):
    step_z = 0 - (i + 1) * 0.18
    create_box(f'Basement_Stair_{i}', (1.2, 0.3, 0.18),
               (0, house_depth/2 - 0.8 - i*0.3, step_z - 0.09),
               material=materials['floor_wood'])

# Storage boxes in basement
create_box('Basement_Box1', (0.4, 0.4, 0.3),
           (-house_width/4, -house_depth/4, basement_z + 0.15),
           material=materials['furniture_dark'])
create_box('Basement_Box2', (0.35, 0.35, 0.25),
           (-house_width/4 + 0.5, -house_depth/4 + 0.3, basement_z + 0.125),
           material=materials['furniture_dark'])

# Leo's body at bottom of stairs (story element)
create_box('Leo_Body', (0.3, 0.6, 0.15),
           (0.3, house_depth/2 - 1.5, basement_z + 0.075),
           material=materials['shirt_red'])

# === GROUND FLOOR ===
ground_z = 0

# Ground floor
create_plane('Ground_Floor', (house_width, house_depth),
             (0, 0, ground_z), material=materials['floor_wood'])

# Exterior walls
create_box('Wall_Ground_Back', (house_width, wall_thickness, floor_height),
           (0, -house_depth/2 + wall_thickness/2, ground_z + floor_height/2),
           material=materials['wall_ext'])
create_box('Wall_Ground_Front', (house_width, wall_thickness, floor_height),
           (0, house_depth/2 - wall_thickness/2, ground_z + floor_height/2),
           material=materials['wall_ext'])
create_box('Wall_Ground_Left', (wall_thickness, house_depth, floor_height),
           (-house_width/2 + wall_thickness/2, 0, ground_z + floor_height/2),
           material=materials['wall_ext'])
create_box('Wall_Ground_Right', (wall_thickness, house_depth, floor_height),
           (house_width/2 - wall_thickness/2, 0, ground_z + floor_height/2),
           material=materials['wall_ext'])

# Interior wall dividing living room and kitchen
create_box('Wall_Ground_Interior', (wall_thickness, house_depth * 0.6, floor_height),
           (0, -house_depth/4, ground_z + floor_height/2),
           material=materials['wall_int'])

# Doorway between rooms (gap in interior wall - represented by two wall segments)
# Already handled by shorter interior wall

# Front door
create_box('Front_Door', (0.1, 0.9, 2.1),
           (0, house_depth/2 - 0.1, ground_z + 1.05),
           material=materials['door'])
# Door frame
create_box('Front_Door_Frame_Top', (1.1, 0.15, 0.1),
           (0, house_depth/2 - 0.1, ground_z + 2.15),
           material=materials['trim'])
create_box('Front_Door_Frame_Left', (0.1, 0.15, 2.1),
           (-0.5, house_depth/2 - 0.1, ground_z + 1.05),
           material=materials['trim'])
create_box('Front_Door_Frame_Right', (0.1, 0.15, 2.1),
           (0.5, house_depth/2 - 0.1, ground_z + 1.05),
           material=materials['trim'])

# Window on front wall (living room side)
window_y = house_depth/2 - 0.1
window_x = -house_width/4
window_z = ground_z + 1.5
create_box('Window_Glass_Front', (0.8, 0.05, 1.0),
           (window_x, window_y, window_z),
           material=materials['glass'])
create_box('Window_Frame_Front_Top', (0.9, 0.1, 0.1),
           (window_x, window_y, window_z + 0.55),
           material=materials['window_frame'])
create_box('Window_Frame_Front_Bottom', (0.9, 0.1, 0.1),
           (window_x, window_y, window_z - 0.55),
           material=materials['window_frame'])

# Ceiling for ground floor
create_plane('Ground_Ceiling', (house_width, house_depth),
             (0, 0, ground_z + floor_height), material=materials['ceiling'])

# === LIVING ROOM FURNITURE ===
living_room_x = -house_width/4
living_room_y = -house_depth/4

# Couch
couch_z = ground_z + 0.4
create_box('Couch_Base', (1.8, 0.8, 0.4),
           (living_room_x, living_room_y + 0.5, couch_z),
           material=materials['furniture_dark'])
create_box('Couch_Back', (1.8, 0.15, 0.6),
           (living_room_x, living_room_y + 0.9, couch_z + 0.3),
           material=materials['furniture_dark'])
create_box('Couch_Arm_Left', (0.15, 0.8, 0.5),
           (living_room_x - 0.85, living_room_y + 0.5, couch_z + 0.25),
           material=materials['furniture_dark'])
create_box('Couch_Arm_Right', (0.15, 0.8, 0.5),
           (living_room_x + 0.85, living_room_y + 0.5, couch_z + 0.25),
           material=materials['furniture_dark'])

# Coffee table
create_box('Coffee_Table_Top', (0.8, 0.5, 0.05),
           (living_room_x, living_room_y - 0.3, ground_z + 0.35),
           material=materials['furniture_light'])
create_box('Coffee_Table_Leg1', (0.05, 0.05, 0.35),
           (living_room_x - 0.35, living_room_y - 0.2, ground_z + 0.175),
           material=materials['furniture_light'])
create_box('Coffee_Table_Leg2', (0.05, 0.05, 0.35),
           (living_room_x + 0.35, living_room_y - 0.2, ground_z + 0.175),
           material=materials['furniture_light'])
create_box('Coffee_Table_Leg3', (0.05, 0.05, 0.35),
           (living_room_x - 0.35, living_room_y - 0.4, ground_z + 0.175),
           material=materials['furniture_light'])
create_box('Coffee_Table_Leg4', (0.05, 0.05, 0.35),
           (living_room_x + 0.35, living_room_y - 0.4, ground_z + 0.175),
           material=materials['furniture_light'])

# TV on stand
tv_stand_z = ground_z + 0.5
create_box('TV_Stand', (0.6, 0.4, 0.5),
           (living_room_x, living_room_y - 1.5, tv_stand_z),
           material=materials['furniture_dark'])
create_box('TV_CRT', (0.5, 0.4, 0.35),
           (living_room_x, living_room_y - 1.5, tv_stand_z + 0.45),
           material=materials['black'])
# TV screen
create_box('TV_Screen', (0.45, 0.05, 0.3),
           (living_room_x, living_room_y - 1.3, tv_stand_z + 0.45),
           material=materials['glass'])

# VCR next to TV
create_box('VCR', (0.3, 0.25, 0.08),
           (living_room_x + 0.4, living_room_y - 1.5, tv_stand_z + 0.04),
           material=materials['black'])

# Carpet
create_plane('LivingRoom_Carpet', (2.0, 1.5),
             (living_room_x, living_room_y, ground_z + 0.01),
             material=materials['carpet_red'])

# === KITCHEN ===
kitchen_y = house_depth/4

# Kitchen counter along back wall
counter_z = ground_z + 0.9
counter_y = -house_depth/2 + 0.6
create_box('Kitchen_Counter_Back', (house_width * 0.4, 0.6, 0.9),
           (0, counter_y, counter_z),
           material=materials['furniture_light'])

# Sink
create_box('Kitchen_Sink', (0.4, 0.35, 0.05),
           (-0.3, counter_y - 0.25, counter_z + 0.475),
           material=materials['metal'])
create_box('Kitchen_Faucet', (0.05, 0.1, 0.3),
           (-0.3, counter_y - 0.35, counter_z + 1.05),
           material=materials['metal'])

# Refrigerator
fridge_z = ground_z + 0.9
create_box('Fridge', (0.6, 0.6, 1.7),
           (house_width/4, counter_y, fridge_z),
           material=materials['white'])
create_box('Fridge_Handle', (0.05, 0.55, 0.15),
           (house_width/4 + 0.31, counter_y - 0.3, fridge_z + 0.85),
           material=materials['metal'])

# Stove
create_box('Stove', (0.55, 0.55, 0.9),
           (0.5, counter_y, counter_z),
           material=materials['metal'])
# Burners
for bx in [-0.2, 0.2]:
    for by in [-0.15, 0.15]:
        create_box(f'Stove_Burner_{bx}_{by}', (0.12, 0.12, 0.03),
                   (0.5 + bx, counter_y + by, counter_z + 0.465),
                   material=materials['black'])

# Dining table
table_z = ground_z + 0.75
table_x = house_width/4
table_y = kitchen_y + 0.5
create_box('Dining_Table_Top', (1.0, 0.6, 0.05),
           (table_x, table_y, table_z),
           material=materials['furniture_light'])
# Table legs
for lx, ly in [(-0.4, -0.25), (0.4, -0.25), (-0.4, 0.25), (0.4, 0.25)]:
    create_box(f'Dining_Table_Leg', (0.06, 0.06, 0.75),
               (table_x + lx, table_y + ly, ground_z + 0.375),
               material=materials['furniture_light'])

# Dining chairs (2 chairs)
for chair_x_offset in [-0.3, 0.3]:
    chair_x = table_x + chair_x_offset
    chair_y = table_y - 0.4
    chair_z = ground_z + 0.45
    create_box(f'Chair_Seat_{chair_x_offset}', (0.35, 0.35, 0.05),
               (chair_x, chair_y, chair_z),
               material=materials['furniture_light'])
    create_box(f'Chair_Back_{chair_x_offset}', (0.35, 0.05, 0.5),
               (chair_x, chair_y - 0.15, chair_z + 0.25),
               material=materials['furniture_light'])
    create_box(f'Chair_Leg_FL_{chair_x_offset}', (0.05, 0.05, 0.45),
               (chair_x - 0.15, chair_y - 0.15, ground_z + 0.225),
               material=materials['furniture_light'])
    create_box(f'Chair_Leg_FR_{chair_x_offset}', (0.05, 0.05, 0.45),
               (chair_x + 0.15, chair_y - 0.15, ground_z + 0.225),
               material=materials['furniture_light'])
    create_box(f'Chair_Leg_BL_{chair_x_offset}', (0.05, 0.05, 0.45),
               (chair_x - 0.15, chair_y + 0.15, ground_z + 0.225),
               material=materials['furniture_light'])
    create_box(f'Chair_Leg_BR_{chair_x_offset}', (0.05, 0.05, 0.45),
               (chair_x + 0.15, chair_y + 0.15, ground_z + 0.225),
               material=materials['furniture_light'])

# === STAIRS TO SECOND FLOOR ===
stairs_start_y = house_depth/2 - 2.0
for i in range(14):
    step_z = ground_z + (i + 1) * 0.18
    step_y = stairs_start_y - i * 0.28
    create_box(f'Stair_{i}', (1.0, 0.28, 0.18),
               (0, step_y, step_z - 0.09),
               material=materials['floor_wood'])

# === SECOND FLOOR ===
second_z = ground_z + floor_height

# Second floor
create_plane('Second_Floor', (house_width, house_depth),
             (0, 0, second_z), material=materials['floor_wood'])

# Exterior walls
create_box('Wall_Second_Back', (house_width, wall_thickness, floor_height),
           (0, -house_depth/2 + wall_thickness/2, second_z + floor_height/2),
           material=materials['wall_ext'])
create_box('Wall_Second_Front', (house_width, wall_thickness, floor_height),
           (0, house_depth/2 - wall_thickness/2, second_z + floor_height/2),
           material=materials['wall_ext'])
create_box('Wall_Second_Left', (wall_thickness, house_depth, floor_height),
           (-house_width/2 + wall_thickness/2, 0, second_z + floor_height/2),
           material=materials['wall_ext'])
create_box('Wall_Second_Right', (wall_thickness, house_depth, floor_height),
           (house_width/2 - wall_thickness/2, 0, second_z + floor_height/2),
           material=materials['wall_ext'])

# Interior walls for bedrooms and bathroom
# Left-right divider
create_box('Wall_Second_LR', (wall_thickness, house_depth * 0.5, floor_height),
           (0, -house_depth/4, second_z + floor_height/2),
           material=materials['wall_int'])

# Bathroom wall
bathroom_z_end = house_depth/2 - 1.5
create_box('Wall_Second_Bathroom', (house_width * 0.35, wall_thickness, floor_height),
           (house_width/4, bathroom_z_end, second_z + floor_height/2),
           material=materials['wall_int'])

# Ceiling for second floor (attic space above)
create_plane('Second_Ceiling', (house_width, house_depth),
             (0, 0, second_z + floor_height), material=materials['ceiling'])

# === LEO'S BEDROOM (Left side, back) ===
leo_room_x = -house_width/4
leo_room_y = -house_depth/4

# Bed
bed_z = second_z + 0.3
create_box('Leo_Bed_Frame', (1.4, 0.8, 0.3),
           (leo_room_x - 0.3, leo_room_y - 0.5, bed_z),
           material=materials['furniture_light'])
create_box('Leo_Mattress', (1.3, 0.7, 0.15),
           (leo_room_x - 0.3, leo_room_y - 0.5, bed_z + 0.225),
           material=materials['bed_sheet'])
create_box('Leo_Pillow', (0.4, 0.3, 0.1),
           (leo_room_x - 0.3, leo_room_y - 0.85, bed_z + 0.375),
           material=materials['white'])
create_box('Leo_Blanket', (1.0, 0.6, 0.1),
           (leo_room_x - 0.3, leo_room_y - 0.3, bed_z + 0.375),
           material=materials['blanket'])

# Reg the stuffed rabbit (on bed)
reg_x = leo_room_x - 0.3
reg_y = leo_room_y - 0.7
reg_z = bed_z + 0.4
create_box('Reg_Body', (0.15, 0.12, 0.18),
           (reg_x, reg_y, reg_z + 0.09),
           material=materials['shirt_red'])  # Red like Leo's shirt
create_box('Reg_Head', (0.12, 0.1, 0.12),
           (reg_x, reg_y - 0.1, reg_z + 0.24),
           material=materials['shirt_red'])
create_box('Reg_Ear_L', (0.04, 0.04, 0.1),
           (reg_x - 0.04, reg_y - 0.12, reg_z + 0.32),
           material=materials['shirt_red'])
create_box('Reg_Ear_R', (0.04, 0.04, 0.1),
           (reg_x + 0.04, reg_y - 0.12, reg_z + 0.32),
           material=materials['shirt_red'])

# Dresser
dresser_z = second_z + 0.5
create_box('Dresser', (0.5, 0.4, 0.8),
           (leo_room_x + 0.8, leo_room_y - 0.8, dresser_z),
           material=materials['furniture_dark'])
# Dresser drawers
for dy in [0.2, -0.1, -0.4]:
    create_box(f'Dresser_Drawer_{dy}', (0.45, 0.05, 0.2),
               (leo_room_x + 0.8, leo_room_y - 0.8 + dy, dresser_z + 0.2),
               material=materials['furniture_light'])

# === RAY & SANDRA'S BEDROOM (Right side, back) ===
parents_room_x = house_width/4
parents_room_y = -house_depth/4

# Larger bed
create_box('Parents_Bed_Frame', (1.8, 0.9, 0.3),
           (parents_room_x, parents_room_y - 0.5, bed_z),
           material=materials['furniture_dark'])
create_box('Parents_Mattress', (1.7, 0.8, 0.15),
           (parents_room_x, parents_room_y - 0.5, bed_z + 0.225),
           material=materials['bed_sheet'])
create_box('Parents_Pillow_L', (0.4, 0.3, 0.1),
           (parents_room_x - 0.35, parents_room_y - 0.85, bed_z + 0.375),
           material=materials['white'])
create_box('Parents_Pillow_R', (0.4, 0.3, 0.1),
           (parents_room_x + 0.35, parents_room_y - 0.85, bed_z + 0.375),
           material=materials['white'])
create_box('Parents_Blanket', (1.4, 0.7, 0.1),
           (parents_room_x, parents_room_y - 0.3, bed_z + 0.375),
           material=materials['furniture_dark'])

# Nightstand
create_box('Nightstand', (0.35, 0.35, 0.5),
           (parents_room_x + 0.7, parents_room_y - 0.5, second_z + 0.25),
           material=materials['furniture_light'])

# === BATHROOM (Right side, front) ===
bathroom_x = house_width/4
bathroom_y = bathroom_z_end + 0.5

# Toilet
toilet_z = second_z + 0.4
create_box('Toilet_Base', (0.35, 0.4, 0.35),
           (bathroom_x - 0.3, bathroom_y - 0.3, toilet_z + 0.175),
           material=materials['toilet'])
create_box('Toilet_Tank', (0.35, 0.15, 0.5),
           (bathroom_x - 0.3, bathroom_y - 0.5, toilet_z + 0.45),
           material=materials['toilet'])
create_box('Toilet_Seat', (0.35, 0.35, 0.05),
           (bathroom_x - 0.3, bathroom_y - 0.25, toilet_z + 0.375),
           material=materials['toilet'])

# Sink vanity
vanity_z = second_z + 0.85
create_box('Vanity', (0.5, 0.45, 0.85),
           (bathroom_x + 0.4, bathroom_y - 0.5, vanity_z),
           material=materials['furniture_light'])
create_box('Sink_Basin', (0.35, 0.3, 0.15),
           (bathroom_x + 0.4, bathroom_y - 0.5, vanity_z + 0.925),
           material=materials['white'])
create_box('Sink_Faucet', (0.05, 0.1, 0.25),
           (bathroom_x + 0.4, bathroom_y - 0.6, vanity_z + 1.025),
           material=materials['metal'])

# Bathtub
tub_z = second_z + 0.45
create_box('Bathtub_Outer', (0.7, 1.4, 0.45),
           (bathroom_x, bathroom_y + 0.5, tub_z + 0.225),
           material=materials['bathtub'])
# Hollow out tub (inner part)
create_box('Bathtub_Inner', (0.6, 1.3, 0.5),
           (bathroom_x, bathroom_y + 0.5, tub_z + 0.25),
           material=materials['bathtub'])

# === ROOF ===
roof_height = 2.0
roof_base_z = second_z + floor_height

# Simple gable roof
roof_y_center = 0
create_box('Roof_Left', (house_width + 0.4, 2.0, roof_height),
           (-0.2, roof_y_center, roof_base_z + roof_height/2),
           material=materials['roof'])
# Rotate to create slope would need mesh manipulation, using box for simplicity

# Join all meshes into one
bpy.ops.object.select_all(action='DESELECT')

# Select all mesh objects
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
for obj in mesh_objects:
    obj.select_set(True)

if len(mesh_objects) > 1:
    # Set active object to the first one
    bpy.context.view_layer.objects.active = mesh_objects[0]
    bpy.ops.object.join()
    joined_obj = bpy.context.active_object
    joined_obj.name = 'Mercer_House'
else:
    joined_obj = mesh_objects[0] if mesh_objects else None
    if joined_obj:
        joined_obj.name = 'Mercer_House'

# Apply smooth shading
if joined_obj:
    bpy.context.view_layer.objects.active = joined_obj
    bpy.ops.object.shade_smooth()

# Export as FBX
bpy.ops.export_scene.fbx(
    filepath='/workspace/mercer_house_final.fbx',
    use_selection=True,
    apply_scale_options='FBX_SCALE_ALL',
    apply_unit_scale=True,
    global_scale=1.0,
    bake_space_transform=True,
    use_mesh_modifiers=True,
)

print("House built and exported successfully!")
print(f"Total meshes created: {len(all_meshes)}")
if joined_obj:
    print(f"Final object: {joined_obj.name}")
    print(f"Vertices: {len(joined_obj.data.vertices)}")
    print(f"Polygons: {len(joined_obj.data.polygons)}")
