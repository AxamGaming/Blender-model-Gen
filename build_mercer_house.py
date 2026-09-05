#!/usr/bin/env python3
"""
THE HOUSE ON MERCER LANE - PSX Style House Builder
Builds the complete house from the narrative document in Blender
Exports as optimized FBX for game use

Based on: THE_HOUSE_ON_MERCER_LANE_v2.md and ART_DIRECTION.md
"""

import bpy
import math
import os

# Clear existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Ensure we have a world environment
if bpy.context.scene.world is None:
    bpy.data.worlds.new("World")
    bpy.context.scene.world = bpy.data.worlds["World"]

# ============================================================================
# CONFIGURATION - Based on ART_DIRECTION.md dimensions
# ============================================================================

# Room dimensions (in meters, 1 Blender unit = 1 meter)
ROOM_DIMS = {
    'living_room': {'width': 5.5, 'depth': 4.5, 'height': 2.4},
    'kitchen': {'width': 3.5, 'depth': 4.0, 'height': 2.4},
    'hallway_ground': {'width': 1.4, 'depth': 2.5, 'height': 2.4},
    'hallway_upstairs': {'width': 1.2, 'depth': 4.0, 'height': 2.2},
    'leo_bedroom': {'width': 2.8, 'depth': 3.2, 'height': 2.2},
    'bathroom': {'width': 1.8, 'depth': 2.4, 'height': 2.2},
    'ray_bedroom': {'width': 3.5, 'depth': 3.8, 'height': 2.2},
    'basement': {'width': 5.0, 'depth': 5.5, 'height': 2.0},
}

# Color Palette - Loop One (Warm, Domestic)
COLORS_LOOP1 = {
    'primary_warm': (0.769, 0.584, 0.416, 1.0),      # #C4956A - wood paneling
    'kitchen_light': (0.910, 0.784, 0.510, 1.0),     # #E8C882 - fluorescent spill
    'shadow_base': (0.173, 0.122, 0.078, 1.0),       # #2C1F14 - dark corners
    'carpet_brown': (0.478, 0.361, 0.243, 1.0),      # #7A5C3E - rental carpet
    'wall_paint': (0.831, 0.769, 0.659, 1.0),        # #D4C4A8 - off-white walls
    'linoleum_grey': (0.541, 0.502, 0.439, 1.0),     # #8A8070 - kitchen floor
    'tv_static': (0.941, 0.929, 0.910, 1.0),         # #F0EDE8 - TV glow
    'accent_rust': (0.545, 0.271, 0.075, 1.0),       # #8B4513 - worn edges
    'leo_shirt_red': (0.800, 0.133, 0.133, 1.0),     # #CC2222 - Leo's shirt
    'vcr_green': (0.0, 1.0, 0.255, 1.0),             # #00FF41 - VCR clock
}

# Color Palette - Loop Three (Desaturated)
COLORS_LOOP3 = {
    'wood_paneling': (0.353, 0.314, 0.282, 1.0),     # #5A5048
    'walls': (0.541, 0.518, 0.502, 1.0),             # #8A8480
    'shadows': (0.098, 0.094, 0.094, 1.0),           # #1A1818
    'concrete_floor': (0.290, 0.267, 0.251, 1.0),    # #4A4440
    'stone_wall': (0.235, 0.220, 0.208, 1.0),        # #3C3835
    'basement_bulb': (0.831, 0.682, 0.376, 1.0),     # #D4AE60 - warm isolated light
    'deep_shadow': (0.059, 0.055, 0.051, 1.0),       # #0F0E0D
}

# ============================================================================
# MATERIAL CREATION
# ============================================================================

def create_material(name, color, roughness=0.8, metallic=0.0):
    """Create a principled BSDF material with given properties."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
    
    return mat

def create_emission_material(name, color, strength=1.0):
    """Create an emission material for lights."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # Remove default node
    if "Principled BSDF" in nodes:
        nodes.remove(nodes["Principled BSDF"])
    
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs['Color'].default_value = color
    emission.inputs['Strength'].default_value = strength
    
    output = nodes.get("Material Output")
    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    return mat

# Create all materials
materials = {}

# Loop 1 materials
materials['wood_paneling'] = create_material('WoodPaneling', COLORS_LOOP1['primary_warm'], roughness=0.7)
materials['wall_paint'] = create_material('WallPaint', COLORS_LOOP1['wall_paint'], roughness=0.9)
materials['carpet'] = create_material('Carpet', COLORS_LOOP1['carpet_brown'], roughness=0.95)
materials['linoleum'] = create_material('Linoleum', COLORS_LOOP1['linoleum_grey'], roughness=0.6)
materials['wood_floor'] = create_material('WoodFloor', (0.65, 0.45, 0.28, 1.0), roughness=0.7)
materials['ceiling'] = create_material('Ceiling', (0.85, 0.82, 0.76, 1.0), roughness=0.9)
materials['leather_couch'] = create_material('LeatherCouch', (0.55, 0.35, 0.25, 1.0), roughness=0.5)
materials['tv_wood'] = create_material('TVWood', (0.35, 0.25, 0.15, 1.0), roughness=0.6)
materials['tv_screen'] = create_emission_material('TVScreen', COLORS_LOOP1['tv_static'], strength=0.5)
materials['vcr_led'] = create_emission_material('VCR_LED', COLORS_LOOP1['vcr_green'], strength=2.0)
materials['kitchen_appliance'] = create_material('KitchenAppliance', (0.92, 0.92, 0.90, 1.0), roughness=0.4)
materials['metal_sink'] = create_material('MetalSink', (0.65, 0.65, 0.68, 1.0), roughness=0.3, metallic=0.8)
materials['glass'] = create_material('Glass', (0.95, 0.95, 0.95, 0.3), roughness=0.1, metallic=0.0)
materials['fabric_curtain'] = create_material('FabricCurtain', (0.70, 0.55, 0.40, 1.0), roughness=0.9)
materials['leo_shirt'] = create_material('LeoShirt', COLORS_LOOP1['leo_shirt_red'], roughness=0.8)
materials['leo_pants'] = create_material('LeoPants', (0.35, 0.40, 0.55, 1.0), roughness=0.8)

# Basement materials
materials['concrete'] = create_material('Concrete', COLORS_LOOP3['concrete_floor'], roughness=0.9)
materials['stone'] = create_material('Stone', COLORS_LOOP3['stone_wall'], roughness=0.95)
materials['basement_bulb'] = create_emission_material('BasementBulb', COLORS_LOOP3['basement_bulb'], strength=3.0)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def add_subdivision_modifier(obj, levels=2, name="Subdivision"):
    """Add subdivision surface modifier for smooth surfaces."""
    mod = obj.modifiers.new(name=name, type='SUBSURF')
    mod.levels = levels
    mod.render_levels = levels
    mod.subdivision_type = 'CATMULL_CLARK'
    return mod

def add_smooth_shade(obj):
    """Apply smooth shading to object."""
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()

def create_box(width, depth, height, location=(0, 0, 0), name="Box"):
    """Create a box mesh with optional subdivision."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (width/2, depth/2, height/2)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def create_plane(width, depth, location=(0, 0, 0), rotation=(0, 0, 0), name="Plane"):
    """Create a plane mesh."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (width/2, depth/2, 1)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def assign_material(obj, mat_name):
    """Assign a material to an object."""
    if mat_name in materials:
        if obj.data.materials:
            obj.data.materials[0] = materials[mat_name]
        else:
            obj.data.materials.append(materials[mat_name])

# ============================================================================
# BUILD ARCHITECTURE
# ============================================================================

def create_room_shell(name, width, depth, height, location, wall_thickness=0.15):
    """Create a room shell with floor, walls, and ceiling."""
    room_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(room_group)
    
    # Floor
    floor = create_plane(width, depth, 
                        location=(location[0], location[1], location[2]), 
                        name=f"{name}_floor")
    assign_material(floor, 'wood_floor' if 'living' in name.lower() or 'bedroom' in name.lower() or 'hallway' in name.lower() else 'linoleum')
    bpy.context.collection.objects.unlink(floor)
    room_group.objects.link(floor)
    
    # Ceiling
    ceiling = create_plane(width, depth, 
                          location=(location[0], location[1], location[2] + height), 
                          name=f"{name}_ceiling")
    assign_material(ceiling, 'ceiling')
    bpy.context.collection.objects.unlink(ceiling)
    room_group.objects.link(ceiling)
    
    # Walls
    # Back wall
    back_wall = create_box(width, wall_thickness, height, 
                          location=(location[0], location[1] - depth/2 + wall_thickness/2, location[2] + height/2),
                          name=f"{name}_wall_back")
    assign_material(back_wall, 'wall_paint')
    bpy.context.collection.objects.unlink(back_wall)
    room_group.objects.link(back_wall)
    
    # Front wall (with opening for doorway)
    if 'bathroom' not in name.lower():
        front_wall_left = create_box(width/2 - 0.6, wall_thickness, height,
                                    location=(location[0] - width/4 - 0.3, location[1] + depth/2 - wall_thickness/2, location[2] + height/2),
                                    name=f"{name}_wall_front_left")
        assign_material(front_wall_left, 'wall_paint')
        bpy.context.collection.objects.unlink(front_wall_left)
        room_group.objects.link(front_wall_left)
        
        front_wall_right = create_box(width/2 - 0.6, wall_thickness, height,
                                     location=(location[0] + width/4 + 0.3, location[1] + depth/2 - wall_thickness/2, location[2] + height/2),
                                     name=f"{name}_wall_front_right")
        assign_material(front_wall_right, 'wall_paint')
        bpy.context.collection.objects.unlink(front_wall_right)
        room_group.objects.link(front_wall_right)
        
        # Door header
        door_header = create_box(1.2, wall_thickness, 0.3,
                                location=(location[0], location[1] + depth/2 - wall_thickness/2, location[2] + height - 1.0),
                                name=f"{name}_door_header")
        assign_material(door_header, 'wall_paint')
        bpy.context.collection.objects.unlink(door_header)
        room_group.objects.link(door_header)
    else:
        front_wall = create_box(width, wall_thickness, height,
                               location=(location[0], location[1] + depth/2 - wall_thickness/2, location[2] + height/2),
                               name=f"{name}_wall_front")
        assign_material(front_wall, 'wall_paint')
        bpy.context.collection.objects.unlink(front_wall)
        room_group.objects.link(front_wall)
    
    # Left wall
    left_wall = create_box(wall_thickness, depth, height,
                          location=(location[0] - width/2 + wall_thickness/2, location[1], location[2] + height/2),
                          name=f"{name}_wall_left")
    assign_material(left_wall, 'wall_paint')
    bpy.context.collection.objects.unlink(left_wall)
    room_group.objects.link(left_wall)
    
    # Right wall
    right_wall = create_box(wall_thickness, depth, height,
                           location=(location[0] + width/2 - wall_thickness/2, location[1], location[2] + height/2),
                           name=f"{name}_wall_right")
    assign_material(right_wall, 'wall_paint')
    bpy.context.collection.objects.unlink(right_wall)
    room_group.objects.link(right_wall)
    
    return room_group

# ============================================================================
# CREATE PROPS
# ============================================================================

def create_couch(location, name="Couch"):
    """Create a PSX-style low-poly couch."""
    couch_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(couch_group)
    
    # Main seat
    seat = create_box(2.2, 0.8, 0.4, 
                     location=(location[0], location[1], location[2] + 0.2),
                     name=f"{name}_seat")
    assign_material(seat, 'leather_couch')
    add_smooth_shade(seat)
    bpy.context.collection.objects.unlink(seat)
    couch_group.objects.link(seat)
    
    # Back rest
    back = create_box(2.2, 0.2, 0.6,
                     location=(location[0], location[1] - 0.4, location[2] + 0.5),
                     name=f"{name}_back")
    assign_material(back, 'leather_couch')
    add_smooth_shade(back)
    bpy.context.collection.objects.unlink(back)
    couch_group.objects.link(back)
    
    # Arm rests
    arm_l = create_box(0.2, 0.8, 0.5,
                      location=(location[0] - 1.0, location[1], location[2] + 0.25),
                      name=f"{name}_arm_left")
    assign_material(arm_l, 'leather_couch')
    add_smooth_shade(arm_l)
    bpy.context.collection.objects.unlink(arm_l)
    couch_group.objects.link(arm_l)
    
    arm_r = create_box(0.2, 0.8, 0.5,
                      location=(location[0] + 1.0, location[1], location[2] + 0.25),
                      name=f"{name}_arm_right")
    assign_material(arm_r, 'leather_couch')
    add_smooth_shade(arm_r)
    bpy.context.collection.objects.unlink(arm_r)
    couch_group.objects.link(arm_r)
    
    # Legs
    for i, lx in enumerate([-0.9, 0.9]):
        for j, ly in enumerate([-0.3, 0.3]):
            leg = create_box(0.1, 0.1, 0.15,
                            location=(lx, location[1] + ly, location[2] + 0.075),
                            name=f"{name}_leg_{i}_{j}")
            assign_material(leg, 'wood_floor')
            bpy.context.collection.objects.unlink(leg)
            couch_group.objects.link(leg)
    
    return couch_group

def create_tv_stand(location, name="TVStand"):
    """Create a particle-board TV stand."""
    stand_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(stand_group)
    
    # Main body
    body = create_box(1.2, 0.5, 0.5,
                     location=(location[0], location[1], location[2] + 0.25),
                     name=f"{name}_body")
    assign_material(body, 'wood_paneling')
    bpy.context.collection.objects.unlink(body)
    stand_group.objects.link(body)
    
    # Legs
    for lx in [-0.5, 0.5]:
        for ly in [-0.2, 0.2]:
            leg = create_box(0.08, 0.08, 0.25,
                            location=(location[0] + lx, location[1] + ly, location[2] + 0.125),
                            name=f"{name}_leg_{lx}_{ly}")
            assign_material(leg, 'wood_paneling')
            bpy.context.collection.objects.unlink(leg)
            stand_group.objects.link(leg)
    
    return stand_group

def create_crt_tv(location, name="CRT_TV"):
    """Create a PS1-era CRT television."""
    tv_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(tv_group)
    
    # Main body (boxy, deep back)
    body = create_box(0.7, 0.6, 0.55,
                     location=(location[0], location[1], location[2] + 0.275),
                     name=f"{name}_body")
    assign_material(body, 'tv_wood')
    bpy.context.collection.objects.unlink(body)
    tv_group.objects.link(body)
    
    # Screen (slightly curved)
    screen = create_plane(0.55, 0.4,
                         location=(location[0], location[1] + 0.3, location[2] + 0.3),
                         rotation=(math.radians(-90), 0, 0),
                         name=f"{name}_screen")
    assign_material(screen, 'tv_screen')
    bpy.context.collection.objects.unlink(screen)
    tv_group.objects.link(screen)
    
    # Screen frame
    frame = create_box(0.58, 0.05, 0.43,
                      location=(location[0], location[1] + 0.275, location[2] + 0.3),
                      name=f"{name}_frame")
    assign_material(frame, 'tv_wood')
    bpy.context.collection.objects.unlink(frame)
    tv_group.objects.link(frame)
    
    return tv_group

def create_vcr(location, name="VCR"):
    """Create a VCR with LED display."""
    vcr_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(vcr_group)
    
    # Main body
    body = create_box(0.35, 0.25, 0.08,
                     location=(location[0], location[1], location[2] + 0.04),
                     name=f"{name}_body")
    assign_material(body, (0.15, 0.15, 0.18, 1.0))
    bpy.context.collection.objects.unlink(body)
    vcr_group.objects.link(body)
    
    # LED display
    led = create_plane(0.08, 0.04,
                      location=(location[0] + 0.12, location[1] + 0.125, location[2] + 0.082),
                      rotation=(math.radians(-90), 0, 0),
                      name=f"{name}_led")
    assign_material(led, 'vcr_led')
    bpy.context.collection.objects.unlink(led)
    vcr_group.objects.link(led)
    
    return vcr_group

def create_coffee_table(location, name="CoffeeTable"):
    """Create a scratched coffee table."""
    table_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(table_group)
    
    # Top
    top = create_box(1.0, 0.6, 0.05,
                    location=(location[0], location[1], location[2] + 0.35),
                    name=f"{name}_top")
    assign_material(top, 'wood_floor')
    bpy.context.collection.objects.unlink(top)
    table_group.objects.link(top)
    
    # Legs
    for lx in [-0.4, 0.4]:
        for ly in [-0.25, 0.25]:
            leg = create_box(0.06, 0.06, 0.35,
                            location=(location[0] + lx, location[1] + ly, location[2] + 0.175),
                            name=f"{name}_leg_{lx}_{ly}")
            assign_material(leg, 'wood_floor')
            bpy.context.collection.objects.unlink(leg)
            table_group.objects.link(leg)
    
    return table_group

def create_kitchen_counter(location, name="KitchenCounter"):
    """Create kitchen counter with sink."""
    counter_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(counter_group)
    
    # Base cabinet
    base = create_box(2.5, 0.6, 0.85,
                     location=(location[0], location[1], location[2] + 0.425),
                     name=f"{name}_base")
    assign_material(base, 'wood_paneling')
    bpy.context.collection.objects.unlink(base)
    counter_group.objects.link(base)
    
    # Countertop
    top = create_box(2.5, 0.65, 0.04,
                    location=(location[0], location[1], location[2] + 0.87),
                    name=f"{name}_top")
    assign_material(top, (0.75, 0.72, 0.68, 1.0))
    bpy.context.collection.objects.unlink(top)
    counter_group.objects.link(top)
    
    return counter_group

def create_refrigerator(location, name="Fridge"):
    """Create a 90s style refrigerator."""
    fridge_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(fridge_group)
    
    # Main body
    body = create_box(0.75, 0.7, 1.6,
                     location=(location[0], location[1], location[2] + 0.8),
                     name=f"{name}_body")
    assign_material(body, 'kitchen_appliance')
    add_smooth_shade(body)
    bpy.context.collection.objects.unlink(body)
    fridge_group.objects.link(body)
    
    # Handle
    handle = create_box(0.05, 0.1, 0.5,
                       location=(location[0] + 0.35, location[1] + 0.35, location[2] + 0.9),
                       name=f"{name}_handle")
    assign_material(handle, 'metal_sink')
    bpy.context.collection.objects.unlink(handle)
    fridge_group.objects.link(handle)
    
    return fridge_group

def create_stove(location, name="Stove"):
    """Create a gas stove with pot."""
    stove_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(stove_group)
    
    # Main body
    body = create_box(0.65, 0.6, 0.9,
                     location=(location[0], location[1], location[2] + 0.45),
                     name=f"{name}_body")
    assign_material(body, 'kitchen_appliance')
    bpy.context.collection.objects.unlink(body)
    stove_group.objects.link(body)
    
    # Burners
    for bx in [-0.2, 0.2]:
        for by in [-0.2, 0.2]:
            burner = create_box(0.12, 0.12, 0.03,
                               location=(location[0] + bx, location[1] + by, location[2] + 0.91),
                               name=f"{name}_burner_{bx}_{by}")
            assign_material(burner, (0.15, 0.15, 0.18, 1.0))
            bpy.context.collection.objects.unlink(burner)
            stove_group.objects.link(burner)
    
    # Pot on stove
    pot = create_box(0.2, 0.2, 0.15,
                    location=(location[0] - 0.2, location[1] - 0.2, location[2] + 1.0),
                    name=f"{name}_pot")
    assign_material(pot, (0.25, 0.25, 0.28, 1.0))
    add_smooth_shade(pot)
    bpy.context.collection.objects.unlink(pot)
    stove_group.objects.link(pot)
    
    # Pot lid
    lid = create_box(0.22, 0.22, 0.03,
                    location=(location[0] - 0.2, location[1] - 0.2, location[2] + 1.08),
                    name=f"{name}_pot_lid")
    assign_material(lid, (0.25, 0.25, 0.28, 1.0))
    bpy.context.collection.objects.unlink(lid)
    stove_group.objects.link(lid)
    
    return stove_group

def create_dining_table(location, name="DiningTable"):
    """Create a 4-person dining table."""
    table_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(table_group)
    
    # Top
    top = create_box(1.2, 0.8, 0.04,
                    location=(location[0], location[1], location[2] + 0.75),
                    name=f"{name}_top")
    assign_material(top, 'wood_floor')
    bpy.context.collection.objects.unlink(top)
    table_group.objects.link(top)
    
    # Legs
    for lx in [-0.5, 0.5]:
        for ly in [-0.35, 0.35]:
            leg = create_box(0.08, 0.08, 0.75,
                            location=(location[0] + lx, location[1] + ly, location[2] + 0.375),
                            name=f"{name}_leg_{lx}_{ly}")
            assign_material(leg, 'wood_floor')
            bpy.context.collection.objects.unlink(leg)
            table_group.objects.link(leg)
    
    return table_group

def create_chair(location, name="Chair"):
    """Create a simple chair."""
    chair_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(chair_group)
    
    # Seat
    seat = create_box(0.4, 0.4, 0.05,
                     location=(location[0], location[1], location[2] + 0.45),
                     name=f"{name}_seat")
    assign_material(seat, 'wood_floor')
    bpy.context.collection.objects.unlink(seat)
    chair_group.objects.link(seat)
    
    # Back
    back = create_box(0.4, 0.05, 0.5,
                     location=(location[0], location[1] - 0.175, location[2] + 0.7),
                     name=f"{name}_back")
    assign_material(back, 'wood_floor')
    bpy.context.collection.objects.unlink(back)
    chair_group.objects.link(back)
    
    # Legs
    for lx in [-0.15, 0.15]:
        for ly in [-0.15, 0.15]:
            leg = create_box(0.05, 0.05, 0.45,
                            location=(location[0] + lx, location[1] + ly, location[2] + 0.225),
                            name=f"{name}_leg_{lx}_{ly}")
            assign_material(leg, 'wood_floor')
            bpy.context.collection.objects.unlink(leg)
            chair_group.objects.link(leg)
    
    return chair_group

def create_bed(location, name="Bed"):
    """Create a child's bed."""
    bed_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(bed_group)
    
    # Frame
    frame = create_box(1.4, 2.2, 0.3,
                      location=(location[0], location[1], location[2] + 0.15),
                      name=f"{name}_frame")
    assign_material(frame, 'wood_floor')
    bpy.context.collection.objects.unlink(frame)
    bed_group.objects.link(frame)
    
    # Mattress
    mattress = create_box(1.3, 2.1, 0.15,
                         location=(location[0], location[1], location[2] + 0.375),
                         name=f"{name}_mattress")
    assign_material(mattress, (0.85, 0.80, 0.75, 1.0))
    add_smooth_shade(mattress)
    bpy.context.collection.objects.unlink(mattress)
    bed_group.objects.link(mattress)
    
    # Pillow
    pillow = create_box(0.5, 0.35, 0.1,
                       location=(location[0], location[1] - 0.8, location[2] + 0.5),
                       name=f"{name}_pillow")
    assign_material(pillow, (0.95, 0.95, 0.95, 1.0))
    add_smooth_shade(pillow)
    bpy.context.collection.objects.unlink(pillow)
    bed_group.objects.link(pillow)
    
    # Blanket
    blanket = create_box(1.0, 1.5, 0.08,
                        location=(location[0], location[1] + 0.2, location[2] + 0.52),
                        name=f"{name}_blanket")
    assign_material(blanket, (0.45, 0.55, 0.75, 1.0))
    add_smooth_shade(blanket)
    bpy.context.collection.objects.unlink(blanket)
    bed_group.objects.link(blanket)
    
    return bed_group

def create_stuffed_rabbit(location, name="Reg"):
    """Create Reg the stuffed rabbit."""
    rabbit_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(rabbit_group)
    
    # Body
    body = create_box(0.15, 0.12, 0.18,
                     location=(location[0], location[1], location[2] + 0.09),
                     name=f"{name}_body")
    assign_material(body, (0.85, 0.75, 0.65, 1.0))
    add_smooth_shade(body)
    bpy.context.collection.objects.unlink(body)
    rabbit_group.objects.link(body)
    
    # Head
    head = create_box(0.12, 0.11, 0.13,
                     location=(location[0], location[1] - 0.08, location[2] + 0.22),
                     name=f"{name}_head")
    assign_material(head, (0.85, 0.75, 0.65, 1.0))
    add_smooth_shade(head)
    bpy.context.collection.objects.unlink(head)
    rabbit_group.objects.link(head)
    
    # Ears
    for ex in [-0.04, 0.04]:
        ear = create_box(0.03, 0.03, 0.1,
                        location=(location[0] + ex, location[1] - 0.12, location[2] + 0.3),
                        name=f"{name}_ear_{ex}")
        assign_material(ear, (0.85, 0.75, 0.65, 1.0))
        add_smooth_shade(ear)
        bpy.context.collection.objects.unlink(ear)
        rabbit_group.objects.link(ear)
    
    return rabbit_group

def create_dresser(location, name="Dresser"):
    """Create a small 3-drawer dresser."""
    dresser_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(dresser_group)
    
    # Main body
    body = create_box(0.8, 0.45, 0.9,
                     location=(location[0], location[1], location[2] + 0.45),
                     name=f"{name}_body")
    assign_material(body, 'wood_paneling')
    bpy.context.collection.objects.unlink(body)
    dresser_group.objects.link(body)
    
    # Drawers (visual only)
    for i in range(3):
        drawer = create_box(0.75, 0.03, 0.25,
                           location=(location[0], location[1] + 0.225, location[2] + 0.2 + i * 0.28),
                           name=f"{name}_drawer_{i}")
        assign_material(drawer, 'wood_paneling')
        bpy.context.collection.objects.unlink(drawer)
        dresser_group.objects.link(drawer)
    
    # Legs
    for lx in [-0.35, 0.35]:
        for ly in [-0.18, 0.18]:
            leg = create_box(0.06, 0.06, 0.1,
                            location=(location[0] + lx, location[1] + ly, location[2] + 0.05),
                            name=f"{name}_leg_{lx}_{ly}")
            assign_material(leg, 'wood_paneling')
            bpy.context.collection.objects.unlink(leg)
            dresser_group.objects.link(leg)
    
    return dresser_group

def create_toilet(location, name="Toilet"):
    """Create a toilet."""
    toilet_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(toilet_group)
    
    # Bowl
    bowl = create_box(0.35, 0.5, 0.3,
                     location=(location[0], location[1], location[2] + 0.15),
                     name=f"{name}_bowl")
    assign_material(bowl, 'kitchen_appliance')
    add_smooth_shade(bowl)
    bpy.context.collection.objects.unlink(bowl)
    toilet_group.objects.link(bowl)
    
    # Tank
    tank = create_box(0.3, 0.2, 0.35,
                     location=(location[0], location[1] - 0.3, location[2] + 0.375),
                     name=f"{name}_tank")
    assign_material(tank, 'kitchen_appliance')
    bpy.context.collection.objects.unlink(tank)
    toilet_group.objects.link(tank)
    
    # Seat
    seat = create_box(0.33, 0.35, 0.03,
                     location=(location[0], location[1], location[2] + 0.32),
                     name=f"{name}_seat")
    assign_material(seat, (0.95, 0.95, 0.95, 1.0))
    bpy.context.collection.objects.unlink(seat)
    toilet_group.objects.link(seat)
    
    return toilet_group

def create_sink_vanity(location, name="SinkVanity"):
    """Create bathroom sink with vanity."""
    vanity_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(vanity_group)
    
    # Cabinet
    cabinet = create_box(0.6, 0.5, 0.75,
                        location=(location[0], location[1], location[2] + 0.375),
                        name=f"{name}_cabinet")
    assign_material(cabinet, 'wood_paneling')
    bpy.context.collection.objects.unlink(cabinet)
    vanity_group.objects.link(cabinet)
    
    # Sink basin
    basin = create_box(0.45, 0.35, 0.15,
                      location=(location[0], location[1], location[2] + 0.82),
                      name=f"{name}_basin")
    assign_material(basin, 'kitchen_appliance')
    add_smooth_shade(basin)
    bpy.context.collection.objects.unlink(basin)
    vanity_group.objects.link(basin)
    
    # Faucet
    faucet = create_box(0.05, 0.1, 0.15,
                       location=(location[0], location[1] - 0.15, location[2] + 0.9),
                       name=f"{name}_faucet")
    assign_material(faucet, 'metal_sink')
    bpy.context.collection.objects.unlink(faucet)
    vanity_group.objects.link(faucet)
    
    # Mirror
    mirror = create_plane(0.5, 0.6,
                         location=(location[0], location[1] - 0.25, location[2] + 1.1),
                         rotation=(math.radians(-90), 0, 0),
                         name=f"{name}_mirror")
    assign_material(mirror, 'glass')
    bpy.context.collection.objects.unlink(mirror)
    vanity_group.objects.link(mirror)
    
    return vanity_group

def create_bathtub(location, name="Bathtub"):
    """Create a bathtub with shower curtain."""
    tub_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(tub_group)
    
    # Tub
    tub = create_box(1.4, 0.7, 0.45,
                    location=(location[0], location[1], location[2] + 0.225),
                    name=f"{name}_tub")
    assign_material(tub, 'kitchen_appliance')
    add_smooth_shade(tub)
    bpy.context.collection.objects.unlink(tub)
    tub_group.objects.link(tub)
    
    # Inside (hollow)
    inside = create_box(1.3, 0.6, 0.4,
                       location=(location[0], location[1], location[2] + 0.23),
                       name=f"{name}_inside")
    assign_material(inside, 'kitchen_appliance')
    bpy.context.collection.objects.unlink(inside)
    tub_group.objects.link(inside)
    
    return tub_group

def create_basement_stairs(location, name="BasementStairs"):
    """Create basement stairs (7 steps)."""
    stairs_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(stairs_group)
    
    step_width = 1.0
    step_depth = 0.25
    step_height = 0.28
    
    for i in range(7):
        step = create_box(step_width, step_depth, step_height,
                         location=(location[0], location[1] - i * step_depth, 
                                  location[2] + (6-i) * step_height + step_height/2),
                         name=f"{name}_step_{i}")
        assign_material(step, 'concrete')
        bpy.context.collection.objects.unlink(step)
        stairs_group.objects.link(step)
    
    return stairs_group

def create_leo_body(location, name="Leo_Body"):
    """Create Leo's body (static mesh for basement)."""
    leo_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(leo_group)
    
    # Torso (lying down)
    torso = create_box(0.25, 0.5, 0.15,
                      location=(location[0], location[1], location[2] + 0.075),
                      name=f"{name}_torso")
    assign_material(torso, 'leo_shirt')
    add_smooth_shade(torso)
    bpy.context.collection.objects.unlink(torso)
    leo_group.objects.link(torso)
    
    # Head
    head = create_box(0.18, 0.2, 0.2,
                     location=(location[0], location[1] + 0.35, location[2] + 0.1),
                     name=f"{name}_head")
    assign_material(head, (0.85, 0.65, 0.55, 1.0))
    add_smooth_shade(head)
    bpy.context.collection.objects.unlink(head)
    leo_group.objects.link(head)
    
    # Legs
    leg_l = create_box(0.12, 0.45, 0.12,
                      location=(location[0] - 0.1, location[1] - 0.3, location[2] + 0.06),
                      name=f"{name}_leg_left")
    assign_material(leg_l, 'leo_pants')
    add_smooth_shade(leg_l)
    bpy.context.collection.objects.unlink(leg_l)
    leo_group.objects.link(leg_l)
    
    leg_r = create_box(0.12, 0.45, 0.12,
                      location=(location[0] + 0.1, location[1] - 0.3, location[2] + 0.06),
                      name=f"{name}_leg_right")
    assign_material(leg_r, 'leo_pants')
    add_smooth_shade(leg_r)
    bpy.context.collection.objects.unlink(leg_r)
    leo_group.objects.link(leg_r)
    
    # Arms
    arm_l = create_box(0.1, 0.35, 0.1,
                      location=(location[0] - 0.2, location[1] + 0.1, location[2] + 0.05),
                      name=f"{name}_arm_left")
    assign_material(arm_l, 'leo_shirt')
    add_smooth_shade(arm_l)
    bpy.context.collection.objects.unlink(arm_l)
    leo_group.objects.link(arm_l)
    
    arm_r = create_box(0.1, 0.35, 0.1,
                      location=(location[0] + 0.2, location[1] + 0.1, location[2] + 0.05),
                      name=f"{name}_arm_right")
    assign_material(arm_r, 'leo_shirt')
    add_smooth_shade(arm_r)
    bpy.context.collection.objects.unlink(arm_r)
    leo_group.objects.link(arm_r)
    
    return leo_group

def create_storage_box(location, name="StorageBox"):
    """Create a cardboard storage box."""
    box_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(box_group)
    
    # Box body
    body = create_box(0.4, 0.3, 0.35,
                     location=(location[0], location[1], location[2] + 0.175),
                     name=f"{name}_body")
    assign_material(body, (0.65, 0.50, 0.35, 1.0))
    bpy.context.collection.objects.unlink(body)
    box_group.objects.link(body)
    
    # Lid (slightly offset)
    lid = create_box(0.42, 0.32, 0.05,
                    location=(location[0], location[1], location[2] + 0.37),
                    name=f"{name}_lid")
    assign_material(lid, (0.60, 0.45, 0.30, 1.0))
    bpy.context.collection.objects.unlink(lid)
    box_group.objects.link(lid)
    
    return box_group

def create_light_bulb(location, name="LightBulb", is_pull_string=False):
    """Create a hanging light bulb."""
    bulb_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(bulb_group)
    
    # Bulb
    bulb = create_box(0.1, 0.1, 0.12,
                     location=(location[0], location[1], location[2]),
                     name=f"{name}_bulb")
    assign_material(bulb, 'basement_bulb')
    add_smooth_shade(bulb)
    bpy.context.collection.objects.unlink(bulb)
    bulb_group.objects.link(bulb)
    
    # Socket
    socket = create_box(0.06, 0.06, 0.08,
                       location=(location[0], location[1], location[2] + 0.1),
                       name=f"{name}_socket")
    assign_material(socket, (0.15, 0.15, 0.18, 1.0))
    bpy.context.collection.objects.unlink(socket)
    bulb_group.objects.link(socket)
    
    if is_pull_string:
        # String
        string = create_box(0.01, 0.01, 0.8,
                           location=(location[0], location[1] + 0.05, location[2] - 0.4),
                           name=f"{name}_string")
        assign_material(string, (0.85, 0.80, 0.75, 1.0))
        bpy.context.collection.objects.unlink(string)
        bulb_group.objects.link(string)
    
    return bulb_group

def create_door(location, rotation_z=0, name="Door", is_open=False):
    """Create a hollow-core door."""
    door_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(door_group)
    
    # Door panel
    panel = create_box(0.8, 0.04, 2.0,
                      location=(location[0], location[1], location[2] + 1.0),
                      name=f"{name}_panel")
    assign_material(panel, (0.75, 0.60, 0.45, 1.0))
    bpy.context.collection.objects.unlink(panel)
    door_group.objects.link(panel)
    
    # Door frame
    frame_top = create_box(0.9, 0.05, 0.05,
                          location=(location[0], location[1], location[2] + 2.0),
                          name=f"{name}_frame_top")
    assign_material(frame_top, (0.65, 0.50, 0.35, 1.0))
    bpy.context.collection.objects.unlink(frame_top)
    door_group.objects.link(frame_top)
    
    frame_left = create_box(0.05, 0.05, 2.0,
                           location=(location[0] - 0.425, location[1], location[2] + 1.0),
                           name=f"{name}_frame_left")
    assign_material(frame_left, (0.65, 0.50, 0.35, 1.0))
    bpy.context.collection.objects.unlink(frame_left)
    door_group.objects.link(frame_left)
    
    frame_right = create_box(0.05, 0.05, 2.0,
                            location=(location[0] + 0.425, location[1], location[2] + 1.0),
                            name=f"{name}_frame_right")
    assign_material(frame_right, (0.65, 0.50, 0.35, 1.0))
    bpy.context.collection.objects.unlink(frame_right)
    door_group.objects.link(frame_right)
    
    # Doorknob
    knob = create_box(0.04, 0.08, 0.04,
                     location=(location[0] + 0.35, location[1] + 0.04, location[2] + 1.0),
                     name=f"{name}_knob")
    assign_material(knob, 'metal_sink')
    add_smooth_shade(knob)
    bpy.context.collection.objects.unlink(knob)
    door_group.objects.link(knob)
    
    return door_group

def create_window(location, width=1.2, height=1.0, name="Window"):
    """Create a window with curtains."""
    window_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(window_group)
    
    # Frame
    frame = create_box(width, 0.08, height,
                      location=location,
                      name=f"{name}_frame")
    assign_material(frame, 'wood_floor')
    bpy.context.collection.objects.unlink(frame)
    window_group.objects.link(frame)
    
    # Glass pane
    glass = create_plane(width - 0.1, height - 0.1,
                        location=(location[0], location[1] + 0.04, location[2]),
                        rotation=(math.radians(-90), 0, 0),
                        name=f"{name}_glass")
    assign_material(glass, 'glass')
    bpy.context.collection.objects.unlink(glass)
    window_group.objects.link(glass)
    
    # Curtains
    curtain_l = create_plane(0.3, height + 0.2,
                            location=(location[0] - width/2 - 0.15, location[1], location[2]),
                            rotation=(math.radians(-90), 0, 0),
                            name=f"{name}_curtain_left")
    assign_material(curtain_l, 'fabric_curtain')
    bpy.context.collection.objects.unlink(curtain_l)
    window_group.objects.link(curtain_l)
    
    curtain_r = create_plane(0.3, height + 0.2,
                            location=(location[0] + width/2 + 0.15, location[1], location[2]),
                            rotation=(math.radians(-90), 0, 0),
                            name=f"{name}_curtain_right")
    assign_material(curtain_r, 'fabric_curtain')
    bpy.context.collection.objects.unlink(curtain_r)
    window_group.objects.link(curtain_r)
    
    return window_group

def create_carpet(location, width, depth, name="Carpet"):
    """Create an area rug."""
    carpet = create_plane(width, depth,
                         location=(location[0], location[1], location[2] + 0.01),
                         name=name)
    assign_material(carpet, 'carpet')
    return carpet

def create_photo_frame(location, name="PhotoFrame"):
    """Create a wall photo frame."""
    frame_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(frame_group)
    
    # Frame border
    border = create_box(0.35, 0.03, 0.25,
                       location=location,
                       name=f"{name}_border")
    assign_material(border, 'wood_floor')
    bpy.context.collection.objects.unlink(border)
    frame_group.objects.link(border)
    
    # Photo (simple colored rectangle for now)
    photo = create_plane(0.3, 0.2,
                        location=(location[0], location[1] + 0.015, location[2]),
                        rotation=(math.radians(-90), 0, 0),
                        name=f"{name}_photo")
    assign_material(photo, (0.75, 0.70, 0.60, 1.0))
    bpy.context.collection.objects.unlink(photo)
    frame_group.objects.link(photo)
    
    return frame_group

def create_fishing_tackle_box(location, name="TackleBox"):
    """Create a plastic fishing tackle box."""
    box_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(box_group)
    
    # Body
    body = create_box(0.35, 0.2, 0.18,
                     location=(location[0], location[1], location[2] + 0.09),
                     name=f"{name}_body")
    assign_material(body, (0.35, 0.45, 0.55, 1.0))
    bpy.context.collection.objects.unlink(body)
    box_group.objects.link(body)
    
    # Lid
    lid = create_box(0.37, 0.22, 0.05,
                    location=(location[0], location[1], location[2] + 0.2),
                    name=f"{name}_lid")
    assign_material(lid, (0.30, 0.40, 0.50, 1.0))
    bpy.context.collection.objects.unlink(lid)
    box_group.objects.link(lid)
    
    # Handle
    handle = create_box(0.15, 0.04, 0.12,
                       location=(location[0], location[1], location[2] + 0.28),
                       name=f"{name}_handle")
    assign_material(handle, (0.15, 0.15, 0.18, 1.0))
    add_smooth_shade(handle)
    bpy.context.collection.objects.unlink(handle)
    box_group.objects.link(handle)
    
    return box_group

def create_shoe(location, name="ChildShoe"):
    """Create a small child's shoe."""
    shoe_group = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(shoe_group)
    
    # Sole
    sole = create_box(0.12, 0.2, 0.05,
                     location=(location[0], location[1], location[2] + 0.025),
                     name=f"{name}_sole")
    assign_material(sole, (0.35, 0.30, 0.25, 1.0))
    add_smooth_shade(sole)
    bpy.context.collection.objects.unlink(sole)
    shoe_group.objects.link(sole)
    
    # Upper
    upper = create_box(0.1, 0.15, 0.1,
                      location=(location[0], location[1] - 0.02, location[2] + 0.1),
                      name=f"{name}_upper")
    assign_material(upper, (0.45, 0.55, 0.75, 1.0))
    add_smooth_shade(upper)
    bpy.context.collection.objects.unlink(upper)
    shoe_group.objects.link(upper)
    
    return shoe_group

# ============================================================================
# MAIN BUILD SEQUENCE
# ============================================================================

print("=" * 60)
print("BUILDING THE HOUSE ON MERCER LANE")
print("=" * 60)

# Set world background
bpy.context.scene.world.color = (0.05, 0.05, 0.05)

# ============================================================================
# FIRST FLOOR
# ============================================================================

first_floor_z = 0.0

# Living Room
print("\nBuilding Living Room...")
living_room = create_room_shell('LivingRoom', 
                                ROOM_DIMS['living_room']['width'],
                                ROOM_DIMS['living_room']['depth'],
                                ROOM_DIMS['living_room']['height'],
                                (0, -2.5, first_floor_z))

# Add carpet
carpet = create_carpet((0, -2.0, first_floor_z + 0.01), 3.5, 3.0, name="LivingRoom_Carpet")
bpy.context.collection.objects.unlink(carpet)
living_room.objects.link(carpet)

# Add couch
couch = create_couch((0, -3.5, first_floor_z), name="LivingRoom_Couch")
for obj in couch.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    living_room.objects.link(obj)

# Add TV stand
tv_stand = create_tv_stand((1.5, -1.5, first_floor_z), name="LivingRoom_TVStand")
for obj in tv_stand.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    living_room.objects.link(obj)

# Add CRT TV
tv = create_crt_tv((1.5, -1.5, first_floor_z + 0.5), name="LivingRoom_TV")
for obj in tv.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    living_room.objects.link(obj)

# Add VCR
vcr = create_vcr((1.5, -1.5, first_floor_z + 1.05), name="LivingRoom_VCR")
for obj in vcr.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    living_room.objects.link(obj)

# Add coffee table
coffee_table = create_coffee_table((-0.5, -1.5, first_floor_z), name="LivingRoom_CoffeeTable")
for obj in coffee_table.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    living_room.objects.link(obj)

# Add window
window = create_window((0, -4.75, first_floor_z + 1.2), width=1.8, height=1.4, name="LivingRoom_Window")
for obj in window.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    living_room.objects.link(obj)

# Add photo frame
photo = create_photo_frame((0, -4.75, first_floor_z + 1.8), name="LivingRoom_Photo")
for obj in photo.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    living_room.objects.link(obj)

# Kitchen
print("Building Kitchen...")
kitchen = create_room_shell('Kitchen',
                           ROOM_DIMS['kitchen']['width'],
                           ROOM_DIMS['kitchen']['depth'],
                           ROOM_DIMS['kitchen']['height'],
                           (-3.5, -2.5, first_floor_z))

# Assign linoleum floor
for obj in kitchen.objects:
    if 'floor' in obj.name.lower():
        assign_material(obj, 'linoleum')

# Add kitchen counter
counter = create_kitchen_counter((-3.5, -4.0, first_floor_z), name="Kitchen_Counter")
for obj in counter.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    kitchen.objects.link(obj)

# Add sink to counter area
sink = create_sink_vanity((-3.5, -4.0, first_floor_z), name="Kitchen_Sink")
for obj in sink.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    kitchen.objects.link(obj)

# Add refrigerator
fridge = create_refrigerator((-5.0, -2.0, first_floor_z), name="Kitchen_Fridge")
for obj in fridge.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    kitchen.objects.link(obj)

# Add stove
stove = create_stove((-2.5, -4.0, first_floor_z), name="Kitchen_Stove")
for obj in stove.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    kitchen.objects.link(obj)

# Add dining table
table = create_dining_table((-4.0, -1.5, first_floor_z), name="Kitchen_Table")
for obj in table.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    kitchen.objects.link(obj)

# Add chairs
chair1 = create_chair((-4.5, -1.0, first_floor_z), name="Kitchen_Chair1")
for obj in chair1.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    kitchen.objects.link(obj)

chair2 = create_chair((-3.5, -1.0, first_floor_z), name="Kitchen_Chair2")
for obj in chair2.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    kitchen.objects.link(obj)

# Hallway (ground floor - leads to basement)
print("Building Ground Hallway...")
hallway_ground = create_room_shell('HallwayGround',
                                   ROOM_DIMS['hallway_ground']['width'],
                                   ROOM_DIMS['hallway_ground']['depth'],
                                   ROOM_DIMS['hallway_ground']['height'],
                                   (-1.75, -0.5, first_floor_z))

# Basement door at end of hallway
basement_door = create_door((-1.75, 0.75, first_floor_z), name="Basement_Door")
for obj in basement_door.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    hallway_ground.objects.link(obj)

# ============================================================================
# STAIRS TO SECOND FLOOR
# ============================================================================

print("Building Stairs...")
stairs_collection = bpy.data.collections.new("Stairs")
bpy.context.scene.collection.children.link(stairs_collection)

stair_width = 1.2
stair_depth = 0.25
stair_height = 0.22
num_stairs = 11

for i in range(num_stairs):
    step = create_box(stair_width, stair_depth, stair_height,
                     location=(-1.0, 0.5 + i * stair_depth, 
                              first_floor_z + ROOM_DIMS['hallway_ground']['height'] + i * stair_height + stair_height/2),
                     name=f"Stairs_step_{i}")
    assign_material(step, 'wood_floor')
    bpy.context.collection.objects.unlink(step)
    stairs_collection.objects.link(step)

# Handrail
for i in range(12):
    post = create_box(0.05, 0.05, 0.9,
                     location=(-1.5, 0.5 + i * stair_depth,
                              first_floor_z + ROOM_DIMS['hallway_ground']['height'] + i * stair_height + 0.45),
                     name=f"Stairs_post_{i}")
    assign_material(post, 'wood_floor')
    bpy.context.collection.objects.unlink(post)
    stairs_collection.objects.link(post)

rail = create_box(0.03, num_stairs * stair_depth, 0.05,
                 location=(-1.55, 0.5 + (num_stairs-1) * stair_depth / 2,
                          first_floor_z + ROOM_DIMS['hallway_ground']['height'] + (num_stairs-1) * stair_height + 0.9),
                 name="Stairs_rail")
assign_material(rail, 'wood_floor')
bpy.context.collection.objects.unlink(rail)
stairs_collection.objects.link(rail)

# ============================================================================
# SECOND FLOOR
# ============================================================================

second_floor_z = first_floor_z + ROOM_DIMS['hallway_ground']['height'] + num_stairs * stair_height

# Upstairs Hallway
print("Building Upstairs Hallway...")
hallway_upstairs = create_room_shell('HallwayUpstairs',
                                     ROOM_DIMS['hallway_upstairs']['width'],
                                     ROOM_DIMS['hallway_upstairs']['depth'],
                                     ROOM_DIMS['hallway_upstairs']['height'],
                                     (0, 3.0, second_floor_z))

# Ray's bedroom door (never opens)
ray_door = create_door((0, 5.2, second_floor_z), name="RayBedroom_Door")
for obj in ray_door.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    hallway_upstairs.objects.link(obj)

# Wedding photo on wall
wedding_photo = create_photo_frame((0, 1.8, second_floor_z + 1.5), name="Hallway_WeddingPhoto")
for obj in wedding_photo.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    hallway_upstairs.objects.link(obj)

# Work boots by wall
boots_l = create_box(0.12, 0.25, 0.1,
                    location=(0.3, 4.5, second_floor_z + 0.05),
                    name="Hallway_Boot_Left")
assign_material(boots_l, (0.35, 0.25, 0.15, 1.0))
add_smooth_shade(boots_l)
bpy.context.collection.objects.unlink(boots_l)
hallway_upstairs.objects.link(boots_l)

boots_r = create_box(0.12, 0.25, 0.1,
                    location=(0.5, 4.5, second_floor_z + 0.05),
                    name="Hallway_Boot_Right")
assign_material(boots_r, (0.35, 0.25, 0.15, 1.0))
add_smooth_shade(boots_r)
bpy.context.collection.objects.unlink(boots_r)
hallway_upstairs.objects.link(boots_r)

# Leo's Bedroom
print("Building Leo's Bedroom...")
leo_bedroom = create_room_shell('LeoBedroom',
                                ROOM_DIMS['leo_bedroom']['width'],
                                ROOM_DIMS['leo_bedroom']['depth'],
                                ROOM_DIMS['leo_bedroom']['height'],
                                (-2.5, 3.5, second_floor_z))

# Bed
bed = create_bed((-2.0, 4.5, second_floor_z), name="LeoBed_Bed")
for obj in bed.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    leo_bedroom.objects.link(obj)

# Reg the rabbit on bed
reg = create_stuffed_rabbit((-2.0, 4.0, second_floor_z + 0.5), name="LeoBed_Reg")
for obj in reg.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    leo_bedroom.objects.link(obj)

# Dresser
dresser = create_dresser((-3.8, 3.5, second_floor_z), name="LeoBed_Dresser")
for obj in dresser.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    leo_bedroom.objects.link(obj)

# Window
bedroom_window = create_window((-4.75, 3.5, second_floor_z + 1.1), width=1.0, height=1.2, name="LeoBed_Window")
for obj in bedroom_window.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    leo_bedroom.objects.link(obj)

# Box under bed
box_under = create_box(0.4, 0.5, 0.2,
                      location=(-2.0, 5.2, second_floor_z + 0.1),
                      name="LeoBed_BoxUnder")
assign_material(box_under, (0.55, 0.40, 0.25, 1.0))
bpy.context.collection.objects.unlink(box_under)
leo_bedroom.objects.link(box_under)

# Bathroom
print("Building Bathroom...")
bathroom = create_room_shell('Bathroom',
                             ROOM_DIMS['bathroom']['width'],
                             ROOM_DIMS['bathroom']['depth'],
                             ROOM_DIMS['bathroom']['height'],
                             (2.0, 2.5, second_floor_z))

# Assign linoleum
for obj in bathroom.objects:
    if 'floor' in obj.name.lower():
        assign_material(obj, 'linoleum')

# Toilet
toilet = create_toilet((2.0, 3.5, second_floor_z), name="Bathroom_Toilet")
for obj in toilet.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    bathroom.objects.link(obj)

# Sink/Vanity
bath_sink = create_sink_vanity((2.5, 2.5, second_floor_z), name="Bathroom_Sink")
for obj in bath_sink.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    bathroom.objects.link(obj)

# Bathtub
bathtub = create_bathtub((1.5, 2.0, second_floor_z), name="Bathroom_Tub")
for obj in bathtub.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    bathroom.objects.link(obj)

# Ray & Sandra's Bedroom (exterior only, door never opens)
print("Building Ray & Sandra's Bedroom...")
ray_bedroom = create_room_shell('RayBedroom',
                                ROOM_DIMS['ray_bedroom']['width'],
                                ROOM_DIMS['ray_bedroom']['depth'],
                                ROOM_DIMS['ray_bedroom']['height'],
                                (2.5, 5.5, second_floor_z))

# Keep door closed
ray_bedroom_door = create_door((2.5, 3.6, second_floor_z), name="RayBedroom_Door_Closed")
for obj in ray_bedroom_door.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    ray_bedroom.objects.link(obj)

# ============================================================================
# BASEMENT
# ============================================================================

basement_z = first_floor_z - ROOM_DIMS['basement']['height']

print("Building Basement...")
basement = create_room_shell('Basement',
                             ROOM_DIMS['basement']['width'],
                             ROOM_DIMS['basement']['depth'],
                             ROOM_DIMS['basement']['height'],
                             (-1.75, 1.5, basement_z))

# Assign concrete/stone materials
for obj in basement.objects:
    if 'floor' in obj.name.lower():
        assign_material(obj, 'concrete')
    elif 'wall' in obj.name.lower() or 'ceiling' in obj.name.lower():
        assign_material(obj, 'stone')

# Basement stairs
basement_stairs = create_basement_stairs((-1.75, 2.5, basement_z), name="Basement_Stairs")
for obj in basement_stairs.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    basement.objects.link(obj)

# Hanging light bulb with pull string
light = create_light_bulb((-1.75, 1.5, basement_z + 1.8), name="Basement_Light", is_pull_string=True)
for obj in light.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    basement.objects.link(obj)

# Storage boxes
storage1 = create_storage_box((-3.0, 0.5, basement_z), name="Basement_Box1")
for obj in storage1.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    basement.objects.link(obj)

storage2 = create_storage_box((-3.5, 1.0, basement_z), name="Basement_Box2")
for obj in storage2.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    basement.objects.link(obj)

storage3 = create_storage_box((-3.0, 2.0, basement_z), name="Basement_Box3")
for obj in storage3.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    basement.objects.link(obj)

# Fishing tackle box
tackle = create_fishing_tackle_box((-4.0, 3.0, basement_z), name="Basement_TackleBox")
for obj in tackle.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    basement.objects.link(obj)

# Child's shoe under stairs
shoe = create_shoe((-1.5, 3.0, basement_z + 0.05), name="Basement_Shoe")
for obj in shoe.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    basement.objects.link(obj)

# Leo's body (far corner)
leo_body = create_leo_body((-4.0, 4.5, basement_z + 0.1), name="Basement_Leo")
for obj in leo_body.objects:
    if obj.name in bpy.context.collection.objects:
        bpy.context.collection.objects.unlink(obj)
    basement.objects.link(obj)

# Covered furniture shapes
covered1 = create_box(0.8, 1.2, 0.6,
                     location=(-3.5, 4.0, basement_z + 0.3),
                     name="Basement_CoveredFurniture1")
assign_material(covered1, (0.75, 0.72, 0.68, 1.0))
add_smooth_shade(covered1)
bpy.context.collection.objects.unlink(covered1)
basement.objects.link(covered1)

# Exposed pipe on ceiling
pipe = create_box(0.08, 4.0, 0.08,
                 location=(-1.75, 1.5, basement_z + 1.95),
                 name="Basement_Pipe")
assign_material(pipe, (0.35, 0.35, 0.38, 1.0))
add_smooth_shade(pipe)
bpy.context.collection.objects.unlink(pipe)
basement.objects.link(pipe)

# ============================================================================
# OPTIMIZATION
# ============================================================================

print("\nOptimizing meshes for PSX aesthetic...")

# Apply modifiers and reduce polygon count where needed
for collection in bpy.data.collections:
    for obj in collection.objects:
        if obj.type == 'MESH':
            # Apply smooth shading to appropriate objects
            if any(keyword in obj.name.lower() for keyword in ['couch', 'bed', 'rabbit', 'pillow', 'blanket', 'bulb']):
                add_smooth_shade(obj)
            
            # Decimate high-poly objects for PSX style
            # (keeping them low-poly from the start, so minimal decimation needed)

# ============================================================================
# EXPORT AS FBX
# ============================================================================

print("\nExporting as FBX...")

# Select all objects in all collections
all_objects = []
for collection in bpy.data.collections:
    for obj in collection.objects:
        all_objects.append(obj)

bpy.ops.object.select_all(action='DESELECT')
for obj in all_objects:
    obj.select_set(True)

# Export settings optimized for game engine import
export_path = '/workspace/mercer_house.fbx'
bpy.ops.export_scene.fbx(
    filepath=export_path,
    use_selection=True,
    apply_scale_options='FBX_SCALE_ALL',
    apply_unit_scale=True,
    bake_space_transform=True,
    object_types={'MESH'},
    use_mesh_modifiers=True,
    mesh_smooth_type='FACE',
    colors_type='SRGB',
    add_leaf_bones=False,
    primary_bone_axis='Y',
    secondary_bone_axis='X',
    use_armature_deform_only=False,
    armature_nodetype='NULL',
    batch_mode='OFF',
    use_subsurf=False,
    use_custom_props=False,
    path_mode='AUTO',
    embed_textures=False,
    use_triangles=True,  # Important for game engines
    use_tspace=False,
    use_mesh_edges=False,
)

print(f"\n{'=' * 60}")
print(f"EXPORT COMPLETE: {export_path}")
print(f"{'=' * 60}")

# Print summary statistics
total_polys = 0
total_verts = 0
for obj in all_objects:
    if obj.type == 'MESH':
        total_polys += len(obj.data.polygons)
        total_verts += len(obj.data.vertices)

print(f"\nModel Statistics:")
print(f"  Total Vertices: {total_verts:,}")
print(f"  Total Polygons: {total_polys:,}")
print(f"  Collections: {len(bpy.data.collections)}")
print(f"\nThe house includes:")
print(f"  - Living Room (with couch, TV, VCR, coffee table)")
print(f"  - Kitchen (with appliances, table, chairs)")
print(f"  - Ground Hallway (with basement door)")
print(f"  - Upstairs Hallway (with Ray's closed door)")
print(f"  - Leo's Bedroom (with bed, Reg, dresser)")
print(f"  - Bathroom (toilet, sink, tub)")
print(f"  - Ray & Sandra's Bedroom (closed)")
print(f"  - Basement (stairs, storage, Leo's body)")
print(f"\nAll meshes use smooth shading and are optimized for PSX-style rendering.")
print(f"Colors follow the Loop One palette (warm, domestic).")
