from __future__ import annotations  
import os, sys, ctypes
sys.path.extend([os.path.join('../', 'lib')])

import bpy 
import bpy_types
import math
from mathutils import Vector
import utilz
# test adding the Planet and Moon class back for proper typing
#from planet import Planet
#from moon import Moon

HELPERS = [
    'frame',
    'frames',
    'get_angle_a',
    'get_angle_b',
    'get_angle_c',
    'normalized_frame'
]

def frame():
    """Returns current blender scene frame"""
    return bpy.context.scene.frame_current

def frames():
    """Returns number of frames in blender scene"""
    return bpy.context.scene.frame_end

def normalized_frame(mini: float = 0.0, maxi: float = math.pi*2, multiplier=1.0) -> float:
    """
    mini: float (Min. value for normalize frame)
    maxi: float (Max. value for normalize frame)
    multiplier: float (normalized_frame*multiplier)
    Returns normalized value for current frame between `mini` and `maxi` values
    """
    mini = float(mini)
    maxi = float(maxi)
    frame = float(bpy.context.scene.frame_current)
    print(f"frame value: {frame}")
    # use standard normalization function with frame values
    print(f"({maxi} - {mini}) * ({frame} - {mini}) / (float(frames()) - 1.00) + {mini}")
    return float(
        multiplier*((maxi - mini) * (frame - mini) / (float(frames()) - float(1)) + mini)
    )

# helper methods for calculating positions, angles, and other things between objects in a blender scene
def distance(v1: mathutils.Vector, v0: mathutils.Vector):
    return math.sqrt(
        ((v1[0]-v0[0])**2) + ((v1[-1] - v0[-1])**2)
    )

def _create_triangular_height(v: mathutils.Vector):
    return (
        Vector(( 
            v[0], 0
        ))
    )

def get_bodies_angular_sweep(name):
    obj = bpy.data.objects[name]
    origin_vector = Vector((0,0))
    position_vector = obj.location.xy
    normal_vector = _create_triangular_height(position_vector)
    o = distance(normal_vector, position_vector)
    a = distance(origin_vector, normal_vector)
    h = distance(origin_vector, position_vector)
    angular_sweep = math.degrees(math.acos(
        o/h
    ))
    # return tuple of o, a, h, angle (degrees)
    print(f"o: {o} a: {a} h: {h}, angle: {angular_sweep}")




# (origin, semi_major_axis) or (0,-semi_major_axis)
# (o, h, a)
# o _create_triangular_height(v: mathutils.Vector):
# h distance(origin, object.xy) 
# a distance(origin, (object.[semimajorAxis],0)

def get_angle_a(a: float,b: float,c: float) -> float:
    """
    a: length of side a
    b: length of side b
    c: length of side c
    Returns angle a per law of cosines
    """
    a = float(a)
    b = float(b)
    c = float(c)
    return float(
        math.degrees( 
            math.acos( (b**2+c**2-a**2) / (2*b*c)  )
            )
        )

def get_angle_b(a: float,b: float,c: float) -> float:
    """
    a: length of side a
    b: length of side b
    c: length of side c
    Returns angle b per law of cosines
    """
    a = float(a)
    b = float(b)
    c = float(c)
    return float(
        math.degrees( 
            math.acos( (a**2+c**2-b**2) / (2*a*c)  )
            )
        )

def get_angle_c(a: float,b: float,c: float) -> float:
    """
    a: length of side a
    b: length of side b
    c: length of side c
    Returns angle c per law of cosines
    """
    a = float(a)
    b = float(b)
    c = float(c)
    return float(
        math.degrees( 
            math.acos( (a**2+b**2-c**2) / (2*a*b)  )
            )
        )

# general blender obj handling 
def deselect_all_objects():
    """deselects all objects in active blender scene"""
    bpy.ops.object.select_all(action='DESELECT')

def select_object(name: str) -> bpy_types.Object:
    """
    name: str (blender object name)
    Selects and Returns requested object if exists
    """
    obj = bpy.context.scene.objects[name]
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj 
    obj.select_set(True)
    return obj

def scene_props(sys_u: str ='METRIC', len_u: str ='KILOMETERS', mass_u: str ='KILOGRAMS', seperate_u: bool = True, scale_u: float = 10000.00, grid_scale: float = 10000.00, f_len: float = 50.0, c_start: float = 100.00, c_end: float = 1000000.00, year_count: int = 20):
    """
    sys_u: str (the system unit setting default: 'METRIC')
    len_u: str (the length unit setting default: 'KILOMETERS')
    mass_u: str (the mass unit setting default: 'KILOGRAMS)
    separate_u: bool (use separate units, EG 100 km 5 m)
    scale_u: float (the global scale of the blend, defines scale for system, length and mass quantities)
    grid_scale: float (the global grid scale, defines scale of grid, how far each grid line is from the other)
    f_len: float (the focal length of the camera)
    c_start: float (the clipping minimum, used for viewing objects in blender)
    c_end: float (the clipping maximum, use for viewing objects in blender)
    year_count: int (multiplier for earth year, 365 frames = 1 year)
    Configures properties and view panel settings with provided scales globally, preset for solar system scales
    """
    bpy.data.scenes["Scene"].unit_settings.system = sys_u
    bpy.data.scenes["Scene"].unit_settings.scale_length = scale_u
    bpy.data.scenes["Scene"].unit_settings.length_unit = len_u
    bpy.data.scenes["Scene"].unit_settings.mass_unit = mass_u
    bpy.data.scenes["Scene"].unit_settings.use_separate = seperate_u 
    bpy.data.scenes["Scene"].use_gravity = False 
    bpy.data.scenes["Scene"].use_nodes = True  
    bpy.data.scenes["Scene"].eevee.use_bloom = True 
    bpy.data.scenes["Scene"].frame_end = 365*year_count
    # remove default objs conditionally
    objs = bpy.data.objects
    if 'Camera' in objs:
        objs.remove(objs['Camera'],do_unlink=True)
    if 'Light' in objs:
        objs.remove(objs['Light'], do_unlink=True)
    if 'Cube' in objs:
        objs.remove(objs['Cube'], do_unlink=True)

    #remove any default materials...
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)

    # NOTE: add a simple light source.
    bpy.ops.object.light_add(type='SUN', radius=10000, location=(0, 0, 0)) 
    bpy.data.objects['Sun'].name = 'FalseSun'
    bpy.data.objects['FalseSun'].data.name = 'FalseSun'
    bpy.data.objects['FalseSun'].data.angle = math.radians(180)

    for workspace in list(bpy.data.workspaces):
        print(f"workspace: {workspace.name}")
        screens = list(workspace.screens)
        for screen in screens:
            print(f"screen: {screen.name}")
            areas = list(screen.areas)
            #screen.shading.type = 'RENDERED'
            for area in areas:
                spaces = area.spaces
                for space in spaces:
                    print(f"space type: {space.type}")
                    if space.type == "VIEW_3D":
                        #space.viewport_shade = 'RENDERED'
                        space.overlay.grid_scale = scale_u 
                        space.overlay.show_axis_x = True 
                        space.overlay.show_axis_y = True
                        space.overlay.show_axis_z = True  
                        space.overlay.show_floor = True
                        space.overlay.show_ortho_grid = True
                        space.lens = f_len 
                        space.clip_start = c_start 
                        space.clip_end = c_end 

def refresh_panels(space_type: str = "PROPERTIES", region_type: str = "WINDOW"):
    """
    space_type: str (type of space to redraw)
    region_type: str (type of region to redraw)
    redraws panels set by parameters 
    """
    for window in list(bpy.context.window_manager.windows):
        for area in list(window.screen.areas):
            if area.spaces[0].type == space_type:
                for region in list(area.regions):
                    if region.type == region_type:
                        region.tag_redraw

def insert_custom_attributes(name: str, planet, debug=True):
    """
    name: str (name of blender object to attach attributes to, note: works for MESH and EMPTY objects currently)
    planet: Planet (pass in the Planet object)
    adds custom attributes from python planet object object to corresponding blender object (parent Empty by default)
    """
    obj = select_object(name)
    for i in planet.keys: 
        print(f"INFO: adding attribute {i} with value {planet.__getattribute__(i)} to {obj.name}") if debug else None
        if obj.type == 'MESH':
            try:
                obj.data[i] = planet.__getattribute__(i) 
            except OverflowError:
                print(f"ERROR: key -> {i} value {planet.__getattribute__(i)} is too large to convert to C int, setting to default {ctypes.c_uint(-1).value}")
                obj[i] =  utilz.make_integer_safe( planet.__getattribute__(i) )#set to max c int
        else:
            try:
                obj[i] = planet.__getattribute__(i) 
            except OverflowError:
                print(f"ERROR: key -> {i} value {planet.__getattribute__(i)} is too large to convert to C int, setting to default {ctypes.c_uint(-1).value}")    
                obj[i] = utilz.make_integer_safe( planet.__getattribute__(i) ) #set to max c int
    refresh_panels()

def add_orbital_drivers(planet) -> bpy_types.Object:
    """
    name: str (name of blender object to attach orbital drivers to, note: this should be a planets parent object and correspond to the python object, by default attached to an EMPTY)
    planet: Planet (pass in the Planet object)
    adds motion drivers (x tranlation, y tranlation, z rotation) to parent empty object for planet
    """
    #planet.englishName
    planetPrimitive = bpy.data.objects[planet.englishName].parent
    xdriver = planetPrimitive.driver_add("location", 0).driver
    ydriver = planetPrimitive.driver_add("location", 1).driver
    zdriver = planetPrimitive.driver_add("rotation_euler", 2).driver 
    # NOTE: x motion driver vars
    semi_major_axis = xdriver.variables.new()
    semi_major_axis.name = "semi_major_axis"
    semi_major_axis.targets[0].id = planetPrimitive
    semi_major_axis.targets[0].data_path = '["semimajorAxis"]'
    harmonic_frequncy = xdriver.variables.new()
    harmonic_frequncy.name = "harmonic_frequency"
    harmonic_frequncy.targets[0].id = planetPrimitive
    harmonic_frequncy.targets[0].data_path = '["harmonicFrequency"]'
    distance_in_au = xdriver.variables.new()
    distance_in_au.name = "distance_in_au"
    distance_in_au.targets[0].id = planetPrimitive
    distance_in_au.targets[0].data_path = '["distanceFromSunInAU"]'
    # NOTE: y motion driver vars
    semi_minor_axis = ydriver.variables.new()
    semi_minor_axis.name = "semi_minor_axis"
    semi_minor_axis.targets[0].id = planetPrimitive 
    semi_minor_axis.targets[0].data_path = '["semiminorAxis"]'
    harmonic_frequncy = ydriver.variables.new()
    harmonic_frequncy.name = "harmonic_frequency"
    harmonic_frequncy.targets[0].id = planetPrimitive
    harmonic_frequncy.targets[0].data_path = '["harmonicFrequency"]'
    distance_in_au = ydriver.variables.new()
    distance_in_au.name = "distance_in_au"
    distance_in_au.targets[0].id = planetPrimitive
    distance_in_au.targets[0].data_path = '["distanceFromSunInAU"]'
    # NOTE: z motion driver vars
    sideral_rot = zdriver.variables.new()
    sideral_rot.name = "sideral_rot"
    sideral_rot.targets[0].id = planetPrimitive
    sideral_rot.targets[0].data_path = '["sideralRotation"]'
    # NOTE: (x,y,z) motion driver expressions
    xdriver.expression = f"(semi_major_axis*(cos((normalized_frame() / distance_in_au))))+0"
    ydriver.expression = f"(semi_minor_axis*(sin((normalized_frame() / distance_in_au))))+0"    
    zdriver.expression = f"(360/sideral_rot)*frame"
    return planetPrimitive


def plot_natural_satellites(planet, sub_divisions: int = 100, prettify: bool = True, debug: bool = False):
    """
    planet: Planet (pass in Planet object)
    sub_divisions: int (the number of divisions to cut plane into)
    prettify: bool (use some fancy logix to try to keep the scene looking good)
    debug: bool (output informational messages)
    adds known natural satellites, an orbital path for each, and adds follow path constraint to satellite object, each object is parented to it's owning planets empty
    NOTE: The follow path constraint is used for orbital motion 
    TODO:  add z-euler rotation driver for axial rotation, add checks for moon limits here, add force fields, fix rotation speeds to be based on the sideralOrbit period for the moon
    """
    moons = planet.moonData
    planetEquaDiameter = planet.equaRadius*2 
    planetMajorAxis = planet.semimajorAxis*2
    planetName = planet.englishName
    print(f"INFO: will process {len(planet.moonData)} moons for {planet.englishName}") if debug else None
    for moon in moons:
        print(f"INFO: processing {moon.englishName}") if debug else None
        # NOTE: if the moons semimajorAxis*2 is less than the planets equaDiameter, the moon will be INSIDE the planet. solution Moon.semimajorAxis=(semimajorAxis*2)+planetEquaDiameter; Moon.semiminorAxis=(semiminorAxis*2)+planetEquaDiameter
        if prettify:
            moonMajorAxis = moon.semimajorAxis*2 
            moonMinorAxis = moon.semiminorAxis*2 
            if moonMajorAxis <= planetEquaDiameter or moonMinorAxis <= planetEquaDiameter:
                moon.semiminorAxis = moon.semiminorAxis+(planetEquaDiameter/2)
                moon.semimajorAxis = moon.semimajorAxis+(planetEquaDiameter/2) 
        # NOTE: construct moons orbital path around its planet, plot elipse, dissolve faces leaving outer connected vertices, convert to path.
        print(f"INFO: configuring the orbital path for {moon.englishName} around {planetName}  (planetEquaDiameter: {planetEquaDiameter}, planetMajorAxis: {planetMajorAxis}) with semimajorAxis ({moon.semimajorAxis}) and semiminorAxis ({moon.semiminorAxis})") if debug else None
        bpy.ops.mesh.primitive_xyz_function_surface(x_eq=f"{moon.semimajorAxis}*(cos(u)*cos(v))", y_eq=f"{moon.semiminorAxis}*(cos(u)*sin(v))", z_eq="0", wrap_u=False, range_v_max=12.5664, close_v=False)
        moonOrbitalPath = bpy.context.active_object
        moonOrbitalPath.name = f"Orbital_Path_{moon.englishName}"
        # NOTE: try setting the origin for objects...
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        diameter = moon.equaRadius*2
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.dissolve_limited()
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.convert(target='CURVE')
        moonOrbitalPath.parent = bpy.data.objects[f"empty_{planet.englishName}"]
        bpy.ops.mesh.primitive_plane_add(size=diameter, enter_editmode=False, location=(0, 0, 0))
        moonObject = bpy.context.active_object 
        moonObject.name = f"moon_{planet.englishName}_{moon.englishName}"
        # add smooth shading and subsurface modifier 
        bpy.ops.object.shade_smooth()
        bpy.ops.object.modifier_add(type='SUBSURF')
        moonObject.modifiers['Subdivision'].levels = 2 
        moonObject.modifiers['Subdivision'].show_only_control_edges = True 
        ##
        # NOTE: try setting the origin for objects...
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        rot_global_radians = float(format(math.radians(90), '.4f'))
        bpy.ops.transform.rotate(value=rot_global_radians, orient_axis='X', orient_type='GLOBAL',
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
            constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False,
            proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
            use_proportional_projected=False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.subdivide(number_cuts=sub_divisions, quadcorner='INNERVERT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.shape_key_add(from_mix=False) 
        #bpy.data.shape_keys["Key"].key_blocks["Plane"].name = "Plane"
        bpy.ops.object.shape_key_add(from_mix=False)
        # return to edite mode
        bpy.ops.object.editmode_toggle() 
        bpy.ops.transform.rotate(value=-rot_global_radians, orient_axis='X', orient_type='GLOBAL',
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
            constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False,
            proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
            use_proportional_projected=False)
        bpy.ops.transform.translate(value=(0, 0, diameter / 2), orient_type='GLOBAL',
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
            constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False,
            proportional_edit_falloff='SMOOTH', proportional_size=1,
            use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.vertex_warp(warp_angle=float(format(math.radians(180), '.4f')),  viewmat=(
            (-2.22045e-16, 0, 1, 0), 
            (1, -2.22045e-16, 0, 0), 
            (0, 1, -2.22045e-16, 0), 
            (-3.9767, -2.02075, -28.9444, 1)
            ),
            center=(0, 0, 0))
        bpy.ops.transform.vertex_warp(warp_angle=float(format(math.radians(360), '.4f')), viewmat=(
            (1, 0, -0, 0), (-0, -1.34359e-07, -1, 0), (0, 1, -1.34359e-07, 0), (-3.75436, -2.02075, 3.9767, 1)),
                                    center=(0, 0, 0))
        bpy.ops.transform.rotate(value=rot_global_radians, orient_axis='X', orient_type='GLOBAL',
                                orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False,
                                proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
                                use_proportional_projected=False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.mode_set(mode='OBJECT')
        key_name = f"Key_{moon.englishName}"
        bpy.data.shape_keys['Key'].name = key_name
        bpy.data.shape_keys[key_name].key_blocks["Basis"].name = f"plane_{moon.englishName}"
        bpy.data.shape_keys[key_name].key_blocks["Key 1"].name = f"planet_{moon.englishName}"
        bpy.data.shape_keys[key_name].key_blocks[f"planet_{moon.englishName}"].value = 1.00
        # use an empty for the moon, to be consistent with the planets 
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=diameter/2, location=(0, 0, 0))
        empty = bpy.context.active_object
        # NOTE: try setting the origin for objects...
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        empty.name = f"empty_{moon.englishName}"
        moonObject.parent = empty 
        empty.parent = bpy.data.objects[f"empty_{planet.englishName}"]
        # end of addition
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        empty.constraints["Follow Path"].target = bpy.data.objects[f"Orbital_Path_{moon.englishName}"]
        empty.constraints["Follow Path"].use_curve_follow = True 
        empty.constraints["Follow Path"].forward_axis = 'FORWARD_Y'
        # TODO: better calculate the influence for constraint 
        empty.constraints["Follow Path"].influence = 0.075
        #empty.constraints["Follow Path"].influence = moon.__class__.normalize_attrib('semimajorAxis', moon.semimajorAxis, start=0.025, end=0.25, precision=5)
        bpy.data.curves[f"Orbital_Path_{moon.englishName}"].path_duration = frames()
        override={'constraint':empty.constraints["Follow Path"]}
        bpy.ops.constraint.followpath_path_animate(override,constraint="Follow Path", owner='OBJECT')
        insert_custom_attributes(f"empty_{moon.englishName}", moon, debug=debug)
        return moonObject

# Planet 'Primitive'
def plot_planet(planet, sub_divisions: int = 100, debug: bool = False):
    """
    planet: Planet (pass in Planet object)
    sub_divisions: int (the number of subdivisions for plane primitive, more divisions for higher quality, but slower render)
    adds planet to scene at origin
    NOTE: you should call Planet.scale_planet() first 
    TODO: axialTilt
    """
    diameter = planet.equaRadius*2
    obj_name = planet.englishName
    rot_global_radians = float(format(math.radians(90), '.4f'))
    bpy.ops.mesh.primitive_plane_add(size=diameter, enter_editmode=False, location=(0, 0, 0))
    plane = bpy.context.active_object
    # NOTE: try setting the origin for objects...
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    plane.name = obj_name
    plane.data.name = f"mesh_{obj_name}"
    # add smooth shading & subsurface modifier
    bpy.ops.object.shade_smooth()
    bpy.ops.object.modifier_add(type='SUBSURF')
    plane.modifiers['Subdivision'].levels = 2 
    plane.modifiers['Subdivision'].show_only_control_edges = True 

    ##
    bpy.ops.transform.rotate(value=rot_global_radians, orient_axis='X', orient_type='GLOBAL',
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
        constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False,
        proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
        use_proportional_projected=False)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.subdivide(number_cuts=sub_divisions, quadcorner='INNERVERT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.shape_key_add(from_mix=False)
    #bpy.data.shape_keys["Key"].key_blocks["Plane"].name = "Plane"
    bpy.ops.object.shape_key_add(from_mix=False)
    #bpy.data.shape_keys["Key"].key_blocks["Planet"].name = "Planet"
    bpy.ops.object.editmode_toggle()
    bpy.ops.transform.rotate(value=-rot_global_radians, orient_axis='X', orient_type='GLOBAL',
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
        constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False,
        proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
        use_proportional_projected=False)
    bpy.ops.transform.translate(value=(0, 0, diameter / 2), orient_type='GLOBAL',
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
        constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False,
        proportional_edit_falloff='SMOOTH', proportional_size=1,
        use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.vertex_warp(warp_angle=float(format(math.radians(180), '.4f')),  viewmat=(
        (-2.22045e-16, 0, 1, 0), 
        (1, -2.22045e-16, 0, 0), 
        (0, 1, -2.22045e-16, 0), 
        (-3.9767, -2.02075, -28.9444, 1)
        ),
        center=(0, 0, 0))
    bpy.ops.transform.vertex_warp(warp_angle=float(format(math.radians(360), '.4f')), viewmat=(
        (1, 0, -0, 0), (-0, -1.34359e-07, -1, 0), (0, 1, -1.34359e-07, 0), (-3.75436, -2.02075, 3.9767, 1)),
                                  center=(0, 0, 0))
    bpy.ops.transform.rotate(value=rot_global_radians, orient_axis='X', orient_type='GLOBAL',
                             orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                             constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False,
                             proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
                             use_proportional_projected=False)
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.mode_set(mode='OBJECT')
    key_name = f"Key_{obj_name}"
    bpy.data.shape_keys['Key'].name = key_name
    bpy.data.shape_keys[key_name].key_blocks["Basis"].name = f"plane_{obj_name}"
    bpy.data.shape_keys[key_name].key_blocks["Key 1"].name = f"planet_{obj_name}"
    bpy.data.shape_keys[key_name].key_blocks[f"planet_{obj_name}"].value = 1.00

    #set rigid, add gravity like force-field
    bpy.ops.rigidbody.objects_add()
    plane.rigid_body.enabled = True
    plane.rigid_body.type = 'ACTIVE'
    plane.rigid_body.mass = planet.massRawKG
    plane.rigid_body.kinematic = True
    plane.rigid_body.friction = 0
    plane.rigid_body.restitution = 0.5 
    plane.rigid_body.collision_shape = 'SPHERE'
    plane.rigid_body.linear_damping = 0  
    plane.rigid_body.angular_damping = 0

    bpy.ops.object.forcefield_toggle()
    plane.field.shape = 'POINT'
    plane.field.type = 'FORCE'
    plane.field.strength = planet.gravity 
    plane.field.use_gravity_falloff = True 

    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=diameter/2, location=(0, 0, 0))
    empty = bpy.context.active_object
    # NOTE: try setting the origin for objects...
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    empty.name = f"empty_{obj_name}"
    plane.parent = empty
    insert_custom_attributes(f"empty_{obj_name}", planet, debug=debug)
    return plane

# Planet 'Sun'
def plot_sun(sun, sub_divisions: int = 100, debug: bool = False):
    """
    sun: Planet (pass in Sun object)
    sub_divisions: int (the number of subdivisions for plane primitive, more divisions for higher quality, but slower render)
    adds sun to scene at origin
    NOTE: you should DEFINITELY call Sun.scale_sun() first 
    TODO: axialTilt
    """
    diameter = sun.equaRadius*2
    obj_name = sun.englishName
    rot_global_radians = float(format(math.radians(90), '.4f'))
    bpy.ops.mesh.primitive_plane_add(size=diameter, enter_editmode=False, location=(0, 0, 0))
    plane = bpy.context.active_object
    # NOTE: try setting the origin for objects...
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    plane.name = obj_name
    plane.data.name = f"mesh_{obj_name}"
    # add smooth shading and subdivision surface modifier for sun
    bpy.ops.object.shade_smooth()
    bpy.ops.object.modifier_add(type='SUBSURF')
    plane.modifiers['Subdivision'].levels = 2 
    plane.modifiers['Subdivision'].show_only_control_edges = True 
    bpy.ops.transform.rotate(value=rot_global_radians, orient_axis='X', orient_type='GLOBAL',
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
        constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False,
        proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
        use_proportional_projected=False)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.subdivide(number_cuts=sub_divisions, quadcorner='INNERVERT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.shape_key_add(from_mix=False)
    bpy.ops.object.shape_key_add(from_mix=False)
    bpy.ops.object.editmode_toggle()
    bpy.ops.transform.rotate(value=-rot_global_radians, orient_axis='X', orient_type='GLOBAL',
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
        constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False,
        proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
        use_proportional_projected=False)
    bpy.ops.transform.translate(value=(0, 0, diameter / 2), orient_type='GLOBAL',
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
        constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False,
        proportional_edit_falloff='SMOOTH', proportional_size=1,
        use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.vertex_warp(warp_angle=float(format(math.radians(180), '.4f')),  viewmat=(
        (-2.22045e-16, 0, 1, 0), 
        (1, -2.22045e-16, 0, 0), 
        (0, 1, -2.22045e-16, 0), 
        (-3.9767, -2.02075, -28.9444, 1)
        ),
        center=(0, 0, 0))
    bpy.ops.transform.vertex_warp(warp_angle=float(format(math.radians(360), '.4f')), viewmat=(
        (1, 0, -0, 0), (-0, -1.34359e-07, -1, 0), (0, 1, -1.34359e-07, 0), (-3.75436, -2.02075, 3.9767, 1)),
                                  center=(0, 0, 0))
    bpy.ops.transform.rotate(value=rot_global_radians, orient_axis='X', orient_type='GLOBAL',
                             orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                             constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False,
                             proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
                             use_proportional_projected=False)
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.mode_set(mode='OBJECT')
    key_name = f"Key_{obj_name}"
    bpy.data.shape_keys['Key'].name = key_name
    bpy.data.shape_keys[key_name].key_blocks["Basis"].name = f"plane_{obj_name}"
    bpy.data.shape_keys[key_name].key_blocks["Key 1"].name = f"star_{obj_name}"
    bpy.data.shape_keys[key_name].key_blocks[f"star_{obj_name}"].value = 1.00
    #set rigid, add gravity like force-field
    bpy.ops.rigidbody.objects_add()
    plane.rigid_body.enabled = True
    plane.rigid_body.type = 'ACTIVE'
    plane.rigid_body.mass = sun.massRawKG
    plane.rigid_body.kinematic = True
    plane.rigid_body.friction = 0
    plane.rigid_body.restitution = 0.5 
    plane.rigid_body.collision_shape = 'SPHERE'
    plane.rigid_body.linear_damping = 0  
    plane.rigid_body.angular_damping = 0
    bpy.ops.object.forcefield_toggle()
    plane.field.shape = 'POINT'
    plane.field.type = 'FORCE'
    plane.field.strength = 100.00 
    plane.field.use_gravity_falloff = True 
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=diameter/2, location=(0, 0, 0))
    empty = bpy.context.active_object
    # NOTE: try setting the origin for objects...
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    empty.name = f"empty_{obj_name}"
    plane.parent = empty
    insert_custom_attributes(f"empty_{obj_name}", sun, debug=debug)
    return plane 

#/Users/photon/Downloads/Spherical/SPACE013SX.hdr
def plot_expanse(file_path):
    bpy.ops.image.open(filepath=file_path, directory=os.path.dirname(file_path), files=[{"name":f"{os.path.basename(file_path)}"}], relative_path=True, show_multiview=False)
    bpy.data.images[f"{os.path.basename(file_path)}"].colorspace_settings.name = 'sRGB'
    bpy.data.images[f"{os.path.basename(file_path)}"].source = 'FILE'
    bpy.data.images[f"{os.path.basename(file_path)}"].filepath = file_path
    # use world node tree 
    worldnodes = bpy.data.worlds['World'].node_tree.nodes 
    worldlinks = bpy.data.worlds['World'].node_tree.links 
    for node in worldnodes:
        worldnodes.remove(node)
    
    environment_texture = worldnodes.new('ShaderNodeTexEnvironment')
    environment_texture.image = bpy.data.images.load( bpy.data.images[f"{os.path.basename(file_path)}"].filepath )
    environment_texture.interpolation = 'Linear'
    environment_texture.projection = 'EQUIRECTANGULAR'
    rgb_curves = worldnodes.new('ShaderNodeRGBCurve')
    # set a point on the color values
    # create 3 points on the color curve.
    list( rgb_curves.mapping.curves[3].points )[0].location = Vector((0.565048, 0.063953))
    list( rgb_curves.mapping.curves[3].points )[1].location = Vector((0.817991, 0.741279))

    #rgb_curves.mapping.curves[3].points.new(position=(0,0))
    #list( rgb_curves.mapping.curves[3].points )[2].location = Vector((0.9100417494773865, 0.9651163816452026))
    node_out = environment_texture.outputs[-1]
    node_in = rgb_curves.inputs[-1]
    worldlinks.new(node_in, node_out)
    # set world outputs
    output = worldnodes.new('ShaderNodeOutputWorld')
    node_in = output.inputs[0]
    node_out = rgb_curves.outputs[0]
    worldlinks.new(node_out, node_in)
    # add environment texture node 
    # add shader node RGB curve 
    # add world output node 


def add_surface_displacement(planet, file_path):
    name = planet.englishName
    # add image to blender
    bpy.ops.image.open(filepath=file_path, directory=os.path.dirname(file_path), files=[{"name":f"{os.path.basename(file_path)}"}], relative_path=True, show_multiview=False)
    bpy.data.images[f"{os.path.basename(file_path)}"].colorspace_settings.name = 'Non-Color'
    bpy.data.images[f"{os.path.basename(file_path)}"].source = 'FILE'
    bpy.data.images[f"{os.path.basename(file_path)}"].filepath = file_path
    #create a texture using the image added
    obj = select_object(name)
    bpy.data.textures.new(f"{obj.name}_bump_data", 'IMAGE')
    bpy.data.textures[f"{obj.name}_bump_data"].image = bpy.data.images[f"{os.path.basename(file_path)}"]
    # add texture for displacement modifier 
    bpy.ops.object.modifier_add(type='DISPLACE')
    obj.modifiers["Displace"].strength = 100.00
    obj.modifiers["Displace"].texture_coords = 'UV'
    obj.modifiers["Displace"].texture = bpy.data.textures[f"{obj.name}_bump_data"]



def add_albedo(planet, file_path):
    name = planet.englishName
    #setup image
    bpy.ops.image.open(filepath=file_path, directory=os.path.dirname(file_path), files=[{"name":f"{os.path.basename(file_path)}"}], relative_path=True, show_multiview=False)
    bpy.data.images[f"{os.path.basename(file_path)}"].colorspace_settings.name = 'sRGB'
    bpy.data.images[f"{os.path.basename(file_path)}"].source = 'FILE'
    bpy.data.images[f"{os.path.basename(file_path)}"].filepath = file_path
    #create a texture using the image added
    obj = select_object(name)
    bpy.ops.material.new()
    bpy.data.materials['Material'].name = f"{obj.name}_albedo"
    material = bpy.data.materials[f"{obj.name}_albedo"] 
    matnodes = bpy.data.materials[f"{obj.name}_albedo"].node_tree.nodes
    nodelinks = bpy.data.materials[f"{obj.name}_albedo"].node_tree.links
    # remove default nodes
    for node in matnodes:
        matnodes.remove(node)
    # add standard albedo setup
    texture_coord = matnodes.new('ShaderNodeTexCoord')
    texture_coord.object = obj
    mapping = matnodes.new('ShaderNodeMapping')
    #rotate the mapping x=90 and z=180 in radians 
    mapping.inputs[2].default_value[0] = round(math.radians(90),3)
    mapping.inputs[2].default_value[2] = round(math.radians(180),3) 
    # connect texture coord with mapping node 
    node_out = texture_coord.outputs[3]
    node_in = mapping.inputs[0]
    nodelinks.new(node_out, node_in)
    # add your base image texture for albedo 
    image_texture = matnodes.new('ShaderNodeTexImage')
    image_texture.image = bpy.data.images.load( bpy.data.images[f"{os.path.basename(file_path)}"].filepath )
    image_texture.interpolation = 'Cubic'
    image_texture.projection = 'SPHERE'
    image_texture.extension = 'EXTEND'
    node_out = mapping.outputs[-1]
    node_in = image_texture.inputs[-1]
    nodelinks.new(node_out, node_in)
    # add bsdf principled shader 
    bsdf_shader = matnodes.new('ShaderNodeBsdfPrincipled')
    node_out = image_texture.outputs[0]
    node_in = bsdf_shader.inputs[0]
    nodelinks.new(node_out, node_in)
    #add material output node 
    output = matnodes.new('ShaderNodeOutputMaterial')
    node_out = bsdf_shader.outputs[-1]
    node_in = output.inputs[0]
    nodelinks.new(node_out, node_in)

    obj.data.materials.append(material)
    return material








