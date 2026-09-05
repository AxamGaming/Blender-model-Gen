import bpy
import math

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Materials
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = color
    return mat

materials = {
    'wall': create_material('Wall', (0.8, 0.75, 0.65, 1.0)),
    'floor_wood': create_material('FloorWood', (0.4, 0.25, 0.15, 1.0)),
    'floor_tile': create_material('FloorTile', (0.3, 0.3, 0.35, 1.0)),
    'ceiling': create_material('Ceiling', (0.9, 0.9, 0.85, 1.0)),
    'door': create_material('Door', (0.35, 0.2, 0.15, 1.0)),
    'furniture': create_material('Furniture', (0.25, 0.15, 0.1, 1.0)),
    'metal': create_material('Metal', (0.6, 0.6, 0.65, 1.0)),
    'white': create_material('White', (0.85, 0.85, 0.85, 1.0)),
    'black': create_material('Black', (0.1, 0.1, 0.1, 1.0)),
    'glass': create_material('Glass', (0.3, 0.5, 0.7, 0.3)),
    'carpet': create_material('Carpet', (0.6, 0.2, 0.2, 1.0)),
    'bed_sheet': create_material('BedSheet', (0.9, 0.9, 0.95, 1.0)),
    'skin': create_material('Skin', (0.9, 0.7, 0.6, 1.0)),
    'hair': create_material('Hair', (0.15, 0.1, 0.05, 1.0)),
}

all_meshes = []

def create_box(name, size, location, material=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    if material:
        obj.data.materials.append(material)
    all_meshes.append(obj)
    return obj

def create_plane(name, size, location, rotation=(0,0,0), material=None):
    bpy.ops.mesh.primitive_plane_add(size=1, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    if material:
        obj.data.materials.append(material)
    all_meshes.append(obj)
    return obj

# House Dimensions
house_width = 10.0
house_depth = 12.0
floor_height = 3.0
wall_thickness = 0.2

# === GROUND FLOOR ===
ground_y = 0.0

create_plane('Ground_Floor', (house_width, house_depth, 1), (0, 0, ground_y), material=materials['floor_wood'])

# Walls - Ground
create_box('Wall_Ground_Back', (house_width, wall_thickness, floor_height), (0, -house_depth/2, ground_y + floor_height/2), material=materials['wall'])
create_box('Wall_Ground_Front', (house_width, wall_thickness, floor_height), (0, house_depth/2, ground_y + floor_height/2), material=materials['wall'])
create_box('Wall_Ground_Left', (wall_thickness, house_depth, floor_height), (-house_width/2, 0, ground_y + floor_height/2), material=materials['wall'])
create_box('Wall_Ground_Right', (wall_thickness, house_depth, floor_height), (house_width/2, 0, ground_y + floor_height/2), material=materials['wall'])

interior_wall_x = -1.5
create_box('Wall_Ground_Interior', (wall_thickness, house_depth * 0.6, floor_height), (interior_wall_x, -house_depth*0.2, ground_y + floor_height/2), material=materials['wall'])

create_plane('Ground_Ceiling', (house_width, house_depth, 1), (0, 0, ground_y + floor_height), material=materials['ceiling'])

# === SECOND FLOOR ===
second_y = ground_y + floor_height

create_plane('Second_Floor', (house_width, house_depth, 1), (0, 0, second_y), material=materials['floor_wood'])

create_box('Wall_Second_Back', (house_width, wall_thickness, floor_height), (0, -house_depth/2, second_y + floor_height/2), material=materials['wall'])
create_box('Wall_Second_Front', (house_width, wall_thickness, floor_height), (0, house_depth/2, second_y + floor_height/2), material=materials['wall'])
create_box('Wall_Second_Left', (wall_thickness, house_depth, floor_height), (-house_width/2, 0, second_y + floor_height/2), material=materials['wall'])
create_box('Wall_Second_Right', (wall_thickness, house_depth, floor_height), (house_width/2, 0, second_y + floor_height/2), material=materials['wall'])

hallway_wall_z = second_y + floor_height/2
create_box('Wall_Second_Hallway', (wall_thickness, house_depth * 0.3, floor_height), (interior_wall_x, -house_depth*0.35, hallway_wall_z), material=materials['wall'])

create_plane('Second_Ceiling', (house_width, house_depth, 1), (0, 0, second_y + floor_height), material=materials['ceiling'])

# === BASEMENT ===
basement_y = ground_y - floor_height

create_plane('Basement_Floor', (house_width * 0.8, house_depth * 0.7, 1), (0, -house_depth*0.1, basement_y), material=materials['floor_tile'])

bw = house_width * 0.8
bd = house_depth * 0.7
create_box('Wall_Basement_Back', (bw, wall_thickness, floor_height), (0, -house_depth*0.1 - bd/2, basement_y + floor_height/2), material=materials['wall'])
create_box('Wall_Basement_Front', (bw, wall_thickness, floor_height), (0, -house_depth*0.1 + bd/2, basement_y + floor_height/2), material=materials['wall'])
create_box('Wall_Basement_Left', (wall_thickness, bd, floor_height), (-bw/2, -house_depth*0.1, basement_y + floor_height/2), material=materials['wall'])
create_box('Wall_Basement_Right', (wall_thickness, bd, floor_height), (bw/2, -house_depth*0.1, basement_y + floor_height/2), material=materials['wall'])

create_plane('Basement_Ceiling', (bw, bd, 1), (0, -house_depth*0.1, basement_y + floor_height), material=materials['ceiling'])

# === STAIRS TO BASEMENT ===
stairs_start_x = 0
stairs_start_z = ground_y
num_steps = 10
step_height = floor_height / num_steps
step_depth = 0.25
for i in range(num_steps):
    step_z = stairs_start_z - (i + 0.5) * step_height
    step_y = -2.0 - i * step_depth
    create_box(f'Basement_Stair_{i}', (2.0, step_depth, step_height), (stairs_start_x, step_y, step_z), material=materials['floor_wood'])

# === FURNITURE - LIVING ROOM ===
couch_x, couch_y, couch_z = -2.5, -3.0, ground_y + 0.4
create_box('Couch_Base', (2.2, 0.8, 0.4), (couch_x, couch_y, couch_z), material=materials['furniture'])
create_box('Couch_Back', (2.2, 0.2, 0.6), (couch_x, couch_y + 0.35, couch_z + 0.3), material=materials['furniture'])
create_box('Couch_Arm_L', (0.2, 0.8, 0.5), (couch_x - 1.0, couch_y, couch_z + 0.25), material=materials['furniture'])
create_box('Couch_Arm_R', (0.2, 0.8, 0.5), (couch_x + 1.0, couch_y, couch_z + 0.25), material=materials['furniture'])

tv_x, tv_y = 3.0, -4.0
create_box('TV_Stand', (0.6, 0.5, 0.5), (tv_x, tv_y, ground_y + 0.25), material=materials['furniture'])
create_box('TV_Box', (0.5, 0.4, 0.35), (tv_x, tv_y - 0.1, ground_y + 0.65), material=materials['black'])
create_plane('TV_Screen', (0.45, 0.3, 1), (tv_x, tv_y - 0.2, ground_y + 0.65), rotation=(0, -math.radians(90), 0), material=materials['glass'])

create_box('Coffee_Table_Top', (1.0, 0.6, 0.05), (0, -2.5, ground_y + 0.35), material=materials['furniture'])
create_box('Coffee_Table_Leg1', (0.05, 0.05, 0.35), (-0.4, -2.2, ground_y + 0.175), material=materials['furniture'])
create_box('Coffee_Table_Leg2', (0.05, 0.05, 0.35), (0.4, -2.2, ground_y + 0.175), material=materials['furniture'])
create_box('Coffee_Table_Leg3', (0.05, 0.05, 0.35), (-0.4, -2.8, ground_y + 0.175), material=materials['furniture'])
create_box('Coffee_Table_Leg4', (0.05, 0.05, 0.35), (0.4, -2.8, ground_y + 0.175), material=materials['furniture'])

create_plane('Living_Carpet', (2.5, 2.0, 1), (0, -2.5, ground_y + 0.01), material=materials['carpet'])

# === KITCHEN ===
counter_y = -5.0
create_box('Kitchen_Counter', (2.5, 0.6, 0.8), (3.5, counter_y, ground_y + 0.4), material=materials['furniture'])
create_box('Kitchen_Sink', (0.4, 0.35, 0.15), (3.5, counter_y - 0.1, ground_y + 0.85), material=materials['metal'])
create_box('Kitchen_Fridge', (0.7, 0.7, 1.6), (2.0, counter_y, ground_y + 0.8), material=materials['white'])
create_box('Kitchen_Stove', (0.6, 0.6, 0.85), (4.5, counter_y, ground_y + 0.425), material=materials['black'])

table_x, table_y = 1.5, -3.5
create_box('Dining_Table_Top', (1.2, 0.8, 0.05), (table_x, table_y, ground_y + 0.7), material=materials['furniture'])
create_box('Dining_Table_Leg1', (0.08, 0.08, 0.7), (table_x - 0.5, table_y - 0.3, ground_y + 0.35), material=materials['furniture'])
create_box('Dining_Table_Leg2', (0.08, 0.08, 0.7), (table_x + 0.5, table_y - 0.3, ground_y + 0.35), material=materials['furniture'])
create_box('Dining_Table_Leg3', (0.08, 0.08, 0.7), (table_x - 0.5, table_y + 0.3, ground_y + 0.35), material=materials['furniture'])
create_box('Dining_Table_Leg4', (0.08, 0.08, 0.7), (table_x + 0.5, table_y + 0.3, ground_y + 0.35), material=materials['furniture'])

chair_x, chair_y = 1.5, -2.8
create_box('Chair_Seat', (0.4, 0.4, 0.05), (chair_x, chair_y, ground_y + 0.4), material=materials['furniture'])
create_box('Chair_Back', (0.4, 0.05, 0.5), (chair_x, chair_y + 0.18, ground_y + 0.65), material=materials['furniture'])
create_box('Chair_Leg1', (0.05, 0.05, 0.4), (chair_x - 0.18, chair_y - 0.18, ground_y + 0.2), material=materials['furniture'])
create_box('Chair_Leg2', (0.05, 0.05, 0.4), (chair_x + 0.18, chair_y - 0.18, ground_y + 0.2), material=materials['furniture'])
create_box('Chair_Leg3', (0.05, 0.05, 0.4), (chair_x - 0.18, chair_y + 0.18, ground_y + 0.2), material=materials['furniture'])
create_box('Chair_Leg4', (0.05, 0.05, 0.4), (chair_x + 0.18, chair_y + 0.18, ground_y + 0.2), material=materials['furniture'])

# === UPSTAIRS - LEO'S BEDROOM ===
leo_room_y = 4.0
leo_room_x = -3.0
bed_y = leo_room_y + 1.0

create_box('Leo_Bed_Frame', (2.0, 1.0, 0.3), (leo_room_x, bed_y, second_y + 0.15), material=materials['furniture'])
create_box('Leo_Mattress', (2.0, 1.0, 0.15), (leo_room_x, bed_y, second_y + 0.375), material=materials['bed_sheet'])
create_box('Leo_Pillow', (0.5, 0.35, 0.1), (leo_room_x, bed_y + 0.4, second_y + 0.5), material=materials['white'])
create_box('Reg_Body', (0.15, 0.1, 0.15), (leo_room_x + 0.5, bed_y + 0.3, second_y + 0.55), material=materials['hair'])
create_box('Reg_Head', (0.12, 0.12, 0.12), (leo_room_x + 0.5, bed_y + 0.35, second_y + 0.65), material=materials['hair'])

create_box('Leo_Dresser', (0.8, 0.5, 0.9), (leo_room_x - 0.8, leo_room_y - 1.5, second_y + 0.45), material=materials['furniture'])

# === UPSTAIRS - PARENTS BEDROOM ===
parents_room_y = -4.0
parents_bed_x = 3.0

create_box('Parents_Bed_Frame', (2.2, 1.4, 0.3), (parents_bed_x, parents_room_y, second_y + 0.15), material=materials['furniture'])
create_box('Parents_Mattress', (2.2, 1.4, 0.15), (parents_bed_x, parents_room_y, second_y + 0.375), material=materials['bed_sheet'])
create_box('Parents_Pillow1', (0.5, 0.35, 0.1), (parents_bed_x - 0.6, parents_room_y + 0.5, second_y + 0.5), material=materials['white'])
create_box('Parents_Pillow2', (0.5, 0.35, 0.1), (parents_bed_x + 0.6, parents_room_y + 0.5, second_y + 0.5), material=materials['white'])

create_box('Nightstand_Left', (0.5, 0.4, 0.5), (parents_bed_x - 1.4, parents_room_y + 0.2, second_y + 0.25), material=materials['furniture'])
create_box('Nightstand_Right', (0.5, 0.4, 0.5), (parents_bed_x + 1.4, parents_room_y + 0.2, second_y + 0.25), material=materials['furniture'])

# === BATHROOM ===
bath_y = 1.0
bath_x = 3.5

create_box('Toilet_Base', (0.35, 0.4, 0.3), (bath_x, bath_y, second_y + 0.15), material=materials['white'])
create_box('Toilet_Tank', (0.35, 0.2, 0.4), (bath_x, bath_y + 0.15, second_y + 0.5), material=materials['white'])
create_box('Toilet_Seat', (0.35, 0.35, 0.05), (bath_x, bath_y - 0.1, second_y + 0.45), material=materials['white'])

create_box('Sink_Vanity', (0.6, 0.5, 0.7), (bath_x + 1.2, bath_y, second_y + 0.35), material=materials['furniture'])
create_box('Sink_Basin', (0.4, 0.3, 0.15), (bath_x + 1.2, bath_y - 0.1, second_y + 0.75), material=materials['white'])

create_box('Bathtub', (1.4, 0.7, 0.5), (bath_x, bath_y - 1.5, second_y + 0.25), material=materials['white'])

# === BASEMENT STORAGE & LEO'S BODY ===
create_box('Box1', (0.4, 0.4, 0.3), (-1.5, -4.0, basement_y + 0.15), material=materials['furniture'])
create_box('Box2', (0.35, 0.35, 0.25), (-1.0, -4.2, basement_y + 0.125), material=materials['furniture'])

create_box('Leo_Body_Torso', (0.25, 0.15, 0.1), (0.5, -5.0, basement_y + 0.05), material=materials['skin'])
create_box('Leo_Body_Head', (0.12, 0.12, 0.12), (0.5, -5.0, basement_y + 0.18), material=materials['skin'])

# === JOIN ALL MESHES INTO ONE ===
print("Joining all meshes into a single solid object...")
bpy.ops.object.select_all(action='DESELECT')
for obj in all_meshes:
    obj.select_set(True)

if len(all_meshes) > 1:
    bpy.context.view_layer.objects.active = all_meshes[0]
    bpy.ops.object.join()
    
    joined_obj = bpy.context.active_object
    joined_obj.name = "Mercer_House"
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.01)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Meshes joined and cleaned up.")

# Apply transforms
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Export FBX
export_path = "/workspace/mercer_house.fbx"
bpy.ops.export_scene.fbx(
    filepath=export_path,
    use_selection=False,
    apply_unit_scale=True,
    apply_scale_options='FBX_SCALE_NONE',
    use_space_transform=True,
    bake_space_transform=True,
    object_types={'MESH'},
    use_mesh_modifiers=True,
    mesh_smooth_type='FACE',
    colors_type='SRGB',
    use_triangles=True,
)
print(f"House exported to {export_path}")

# Stats
total_polys = 0
total_verts = 0
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        total_polys += len(obj.data.polygons)
        total_verts += len(obj.data.vertices)

print(f"\nModel Statistics:")
print(f"  Total Vertices: {total_verts:,}")
print(f"  Total Polygons: {total_polys:,}")
