from __future__ import annotations  
import os, sys, ctypes
sys.path.extend([os.path.join('../', 'lib')])

import bpy 
import bpy_types
import math, mathutils
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

def scene_props(sys_u: str ='METRIC', len_u: str ='KILOMETERS', mass_u: str ='KILOGRAMS', seperate_u: bool = True, scale_u: float = 10000.00, grid_scale: float = 10000.00, f_len: float = 50.0, c_start: float = 100.00, c_end: float = 1000000.00, year_count: int = 5, output_file='/Users/photon/Downloads/ss.mp4', output_fmt='MPEG4', output_encoder='FFMPEG'):
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
    bpy.data.scenes["Scene"].eevee.use_gtao = True
    bpy.data.scenes["Scene"].eevee.use_ssr = True
    bpy.data.scenes["Scene"].eevee.use_ssr_refraction = True
    bpy.data.scenes["Scene"].eevee.ssr_quality = 0.5
    bpy.data.scenes["Scene"].eevee.use_motion_blur = True
    bpy.data.scenes["Scene"].eevee.volumetric_end = 300000
    bpy.data.scenes["Scene"].eevee.volumetric_tile_size = '16'
    bpy.data.scenes["Scene"].eevee.use_volumetric_shadows = True
    bpy.data.scenes["Scene"].render.filepath = output_file 
    bpy.data.scenes["Scene"].render.image_settings.file_format = output_encoder
    #bpy.data.scenes["Scene"].format = output_fmt  
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
    bpy.data.lights['FalseSun'].energy = 2.5

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
                #attr = planet.__getattribute__(i) 
                #if str(attr).replace('.','').isdigit():
                #    obj.data[i] = float(attr)
                #else:
                #    obj.data[i] = attr
                print(f"INFO: attr key -> {i}, attr value -> {planet.__getattribute__(i)}, attr type -> {type(planet.__getattribute__(i))}") if debug else None
                attr = planet.__getattribute__(i)
                if isinstance(attr, int):
                    attr = float(attr)

                
                #obj.data[i] = planet.__getattribute__(i) 
                obj.data[i] = attr
            except OverflowError:
                print(f"ERROR: key -> {i} value {planet.__getattribute__(i)} is too large to convert to C int, setting to default {ctypes.c_uint(-1).value}")
                obj.data[i] =  utilz.make_integer_safe( planet.__getattribute__(i) )#set to max c int
        else:
            try:
                #attr = planet.__getattribute__(i) 
                #if str(attr).replace('.', '').isdigit():
                #    obj.data[i] = float(attr)
                #else:
                #    obj.data[i] = attr
                #print(f"i key: {i}")
                print(f"INFO: attr key -> {i}, attr value -> {planet.__getattribute__(i)}, attr type -> {type(planet.__getattribute__(i))}") if debug else None
                attr = planet.__getattribute__(i)
                if isinstance(attr, int):
                    attr = float(attr)

                
                #obj.data[i] = planet.__getattribute__(i) 
                obj[i] = attr
                #print(f"i key: {i} i value: {planet.__getattribute__(i)} i type: {type(planet.__getattribute__(i))}")
                #obj[i] = planet.__getattribute__(i) 
            except OverflowError:
                print(f"ERROR: key -> {i} value {planet.__getattribute__(i)} is too large to convert to C int, setting to default {ctypes.c_uint(-1).value}")    
                obj[i] = utilz.make_integer_safe( planet.__getattribute__(i) ) #set to max c int
    refresh_panels()

def add_planet_trackcam(planet): 
    bpy_planet = bpy.data.objects[planet.englishName]
    bpy_planet_parent = bpy.data.objects[planet.englishName].parent
    #step 1, add a camera to the scene at origin 
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(0.0, 0.0, 0.0))
    camera = bpy.data.objects['Camera']
    camera.name = f"camera_{planet.englishName}"
    camera.data.dof.use_dof = True 
    camera.data.display_size = 1e5
    camera.data.show_sensor = True 
    camera.data.show_limits = True 
    camera.data.clip_start = 25e3
    camera.data.clip_end = 1e6
    camera.data.dof.focus_object = bpy_planet
    #set camera rotation such that it properly tracks planet
    #camera.rotation_euler[0] = math.radians(180)
    #camera.rotation_euler[1] = math.radians(180)
    bpy.ops.object.constraint_add(type='TRACK_TO')
    camera.constraints['Track To'].target = bpy_planet
    camera.constraints['Track To'].target_space = 'LOCAL'
    camera.constraints['Track To'].owner_space = 'LOCAL'
    camera.constraints['Track To'].influence = 1. 
    camera.constraints['Track To'].up_axis = 'UP_Y'
    camera.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
    camera.constraints['Track To'].use_target_z = False

    
    #camera.parent = planet 
    xdriver = camera.driver_add("location", 0).driver
    ydriver = camera.driver_add("location", 1).driver
    lensdriver = camera.data.driver_add('lens').driver 
    lensdriver.expression = f" -50*cos(0.005*frame/2) if cos(0.005*frame/2) < 0 else 50*cos(0.005*frame/2)"
    # NOTE: x motion driver vars
    semi_major_axis = xdriver.variables.new()
    semi_major_axis.name = "semi_major_axis"
    semi_major_axis.targets[0].id = bpy_planet_parent
    semi_major_axis.targets[0].data_path = '["semimajorAxis"]'
    harmonic_frequncy = xdriver.variables.new()
    harmonic_frequncy.name = "harmonic_frequency"
    harmonic_frequncy.targets[0].id = bpy_planet_parent
    harmonic_frequncy.targets[0].data_path = '["harmonicFrequency"]'
    distance_in_au = xdriver.variables.new()
    distance_in_au.name = "distance_in_au"
    distance_in_au.targets[0].id = bpy_planet_parent
    distance_in_au.targets[0].data_path = '["distanceFromSunInAU"]'
    # NOTE: y motion drivers 
    semi_minor_axis = ydriver.variables.new()
    semi_minor_axis.name = "semi_minor_axis"
    semi_minor_axis.targets[0].id = bpy_planet_parent
    semi_minor_axis.targets[0].data_path = '["semiminorAxis"]'
    harmonic_frequncy = ydriver.variables.new()
    harmonic_frequncy.name = "harmonic_frequency"
    harmonic_frequncy.targets[0].id = bpy_planet_parent
    harmonic_frequncy.targets[0].data_path = '["harmonicFrequency"]'
    distance_in_au = ydriver.variables.new()
    distance_in_au.name = "distance_in_au"
    distance_in_au.targets[0].id = bpy_planet_parent
    distance_in_au.targets[0].data_path = '["distanceFromSunInAU"]'
    xdriver.expression = f"((semi_major_axis*1.5)*(cos((normalized_frame() / distance_in_au))))+0"
    ydriver.expression = f"((semi_minor_axis*1.5)*(sin((normalized_frame() / distance_in_au))))+0"    
    return xdriver, ydriver


def add_orbital_drivers(planet):
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
    return xdriver, ydriver, zdriver


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

        # improve path settings
        moonOrbitalPath.data.path_duration = moon.sideralOrbit 
        moonOrbitalPath.data.resolution_u = 128  
        moonOrbitalPath.data.render_resolution_u = 128
        moonOrbitalPath.data.twist_smooth = 1. 
        moonOrbitalPath.data.splines[0].use_smooth = True 

        bpy.ops.mesh.primitive_plane_add(size=diameter, enter_editmode=False, location=(0, 0, 0))
        moonObject = bpy.context.active_object 
        moonObject.name = f"{moon.englishName}"
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

def plot_atmosphere(planet, sub_divisions: int = 100, black_val: float = 0.460, white_val: float = 0.640, noise_scale: float = 9.6, noise_detail: float = 11.4, debug: bool = False ):
    """
    Plots an atmosphere for a given planet
    """
    diameter = (planet.equaRadius*2+((planet.equaRadius*2)*0.1))
    planetobj = bpy.data.objects[planet.englishName]
    obj_name = f"atmos_{planet.englishName}"

    rot_global_radians = float(format(math.radians(90), '.4f'))
    bpy.ops.mesh.primitive_plane_add(size=diameter, enter_editmode=False, location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.name = obj_name
    plane.data.name = f"mesh_{obj_name}"
    # add smooth shading & subsurface modifier
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
    bpy.data.shape_keys[key_name].key_blocks["Basis"].name = f"plane_atmos_{obj_name}"
    bpy.data.shape_keys[key_name].key_blocks["Key 1"].name = f"sphere_atmos_{obj_name}"
    bpy.data.shape_keys[key_name].key_blocks[f"sphere_atmos_{obj_name}"].value = 1.00
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    empty = bpy.data.objects[f"empty_{planet.englishName}"]
    plane.parent = empty 
    #do materials
    bpy.ops.material.new()
    bpy.data.materials['Material'].name = f"{planetobj.name}_atmos"
    material = bpy.data.materials[f"{planetobj.name}_atmos"] 
    material.blend_method = 'HASHED'
    material.shadow_method = 'CLIP'
    material.use_backface_culling = True
    material.use_screen_refraction = True
    matnodes = bpy.data.materials[f"{planetobj.name}_atmos"].node_tree.nodes
    nodelinks = bpy.data.materials[f"{planetobj.name}_atmos"].node_tree.links    
    for node in matnodes:
        matnodes.remove(node)
    noise = matnodes.new('ShaderNodeTexNoise')
    colorramp = matnodes.new('ShaderNodeValToRGB')
    pbsdf = matnodes.new('ShaderNodeBsdfPrincipled')
    transparent = matnodes.new('ShaderNodeBsdfTransparent')
    mix = matnodes.new('ShaderNodeMixShader')
    output = matnodes.new('ShaderNodeOutputMaterial')
    noise.inputs[2].default_value = noise_scale
    noise.inputs[3].default_value = noise_detail
    elements = colorramp.color_ramp.elements 
    elements[0].position = black_val
    elements[1].position = white_val
    pbsdf.inputs[7].default_value = 1.
    node_out = noise.outputs[-1]
    node_in = colorramp.inputs[0]
    #connect noise to ramp
    nodelinks.new(node_out, node_in)
    #connect ramp to bsdf 
    node_out = colorramp.outputs[0]
    node_in = pbsdf.inputs[0]
    nodelinks.new(node_out, node_in)
    #connect bsdf to first input on mix 
    node_out = pbsdf.outputs[0]
    node_in = mix.inputs[1]
    nodelinks.new(node_out, node_in)

    #connect transparent bsdf to mix 
    node_out = transparent.outputs[0]
    node_in = mix.inputs[2]
    nodelinks.new(node_out, node_in)
    #connect mix to output 
    node_out = mix.outputs[0]
    node_in = output.inputs[0]
    nodelinks.new(node_out, node_in)
    plane.data.materials.append(material)

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


def add_surface_displacement(planet, file_path, strength=30.):
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
    obj.modifiers["Displace"].strength = strength
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
    material.blend_method = 'HASHED'
    material.shadow_method = 'CLIP'
    material.use_backface_culling = True
    material.use_screen_refraction = True
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
    bsdf_shader.inputs[7].default_value = 1.
    bsdf_shader.inputs[11].default_value = 0.
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

def sun_texture(sun, texture):
    name = sun.englishName
    base_img_path = texture.textures[name]['albedo']
    bpy.data.images.load(base_img_path, check_existing=False)
    base_img = bpy.data.images[f"{os.path.basename(base_img_path)}"]
    base_img.name = f"{sun.englishName}_albedo"
    base_img.colorspace_settings.name = 'sRGB'
    base_img.source = 'FILE'
    base_img.filepath = base_img_path
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
    #image_texture.image = bpy.data.images.load( bpy.data.images[f"{os.path.basename(base_img_path)}"].filepath , check_existing=True)
    image_texture.image = bpy.data.images.load( bpy.data.images[f"{obj.name}_albedo"].filepath, check_existing=True) 
    image_texture.interpolation = 'Cubic'
    image_texture.projection = 'SPHERE'
    image_texture.extension = 'EXTEND'
    node_out = mapping.outputs[-1]
    node_in = image_texture.inputs[-1]
    nodelinks.new(node_out, node_in)
    # add bsdf principled shader 


    # add hue saturation and bump node 
    bsdf_shader = matnodes.new('ShaderNodeBsdfPrincipled')
    hue = matnodes.new('ShaderNodeHueSaturation')
    bump = matnodes.new('ShaderNodeBump')
    hue.inputs[0].default_value = 0.49

    #connect image texture to hue sat 
    node_out = image_texture.outputs[0]
    node_in = hue.inputs[4]
    nodelinks.new(node_out, node_in)

    #connect hue sat to principled BSDF 
    #node_out = hue.outputs[0]
    #node_in = bsdf_shader.inputs[0]
    #node_in_2 = bsdf_shader.inputs[17]
    #nodelinks.new(node_out, node_in)
    #nodelinks.new(node_out, node_in_2)

    #connect image texture to bump 
    node_out = image_texture.outputs[0]
    node_in = bump.inputs[2]
    nodelinks.new(node_out, node_in)

    #connect bump to BSDF normal input 
    node_out = bump.outputs[0]
    node_in = bsdf_shader.inputs[19]
    nodelinks.new(node_out, node_in)


    #
    #node_out = image_texture.outputs[0]
    #node_in = bsdf_shader.inputs[0]
    #nodelinks.new(node_out, node_in)


    noise = matnodes.new('ShaderNodeTexNoise')
    noise.noise_dimensions = '2D'
    noise.inputs[2].default_value = 45.
    noise.inputs[3].default_value = 32.

    colorramp = matnodes.new('ShaderNodeValToRGB')
    elements = colorramp.color_ramp.elements 

    # set black position
    elements[0].position = 0.310

    # add 3 points for sun primary colors to ramp
    elements.new(position=0.5)
    
    #bpy.data.materials["Sun_albedo"].node_tree.nodes["ColorRamp"].color_ramp.elements[1].color = (1, 0.0448805, 0.0203759, 1)

    # reds 
    elements[1].color = (1, 0.0448805, 0.0203759, 1)
    elements[1].position = 0.414

    # oranges
    #bpy.data.materials["Sun_albedo"].node_tree.nodes["ColorRamp"].color_ramp.elements[2].color = (1, 0.214121, 0.0093381, 1)

    elements.new(position=0.5)
    elements[2].color = (1, 0.214121, 0.0093381, 1)
    elements[2].position = 0.515

    #yellows
    #bpy.data.materials["Sun_albedo"].node_tree.nodes["ColorRamp"].color_ramp.elements[3].color = (1, 0.912944, 0.0046465, 1)

    elements.new(position=0.5)
    elements[3].position = 0.585
    elements[3].color = (1, 0.912944, 0.0046465, 1)
    #elements[0].position = 
    elements[-1].position = 0.678


    node_out = noise.outputs[1]
    node_in = colorramp.inputs[0]
    nodelinks.new(node_out, node_in)


    mix = matnodes.new('ShaderNodeMixRGB')
    mix.blend_type = 'ADD'


    #hue to mix 
    node_out = hue.outputs[0]
    node_in = mix.inputs[1]
    nodelinks.new(node_out, node_in)

    #ramp to mix 
    node_out = colorramp.outputs[0]
    node_in = mix.inputs[2]
    nodelinks.new(node_out, node_in)

    #add material output node 
    output = matnodes.new('ShaderNodeOutputMaterial')
    node_out = bsdf_shader.outputs[-1]
    node_in = output.inputs[0]
    nodelinks.new(node_out, node_in)

    #mix goes to base color and emission now 
    node_out = mix.outputs[0]
    node_in = bsdf_shader.inputs[0] #base color 
    node_in_2 = bsdf_shader.inputs[17]
    nodelinks.new(node_out, node_in)
    nodelinks.new(node_out, node_in_2)

    #settings for bsdf_shader 
    bsdf_shader.inputs[5].default_value = 0. #specular 
    bsdf_shader.inputs[7].default_value = 1. #roughness 
    bsdf_shader.inputs[11].default_value = 0. #sheen tint

    fresnel = matnodes.new('ShaderNodeFresnel')
    fresnel.inputs[0].default_value = 0.98
    emission = matnodes.new('ShaderNodeEmission')
    mix_shader = matnodes.new('ShaderNodeMixShader')
    #bpy.data.materials["Sun_albedo"].node_tree.nodes["Emission.001"].inputs[0].default_value = (1, 0.287624, 0.00289602, 1)

    emission.inputs[0].default_value = (1, 0.287624, 0.00289602, 1)

    #connect fresnel to factor input of mix shader 
    node_out = fresnel.outputs[0]
    node_in = mix_shader.inputs[0]
    nodelinks.new(node_out, node_in)

    #connect emission to first shader mix input 
    node_out = bsdf_shader.outputs[0]
    node_in = mix_shader.inputs[1]
    nodelinks.new(node_out, node_in)


    #connect BSDF to second shader mix input 
    node_out = emission.outputs[0]
    node_in = mix_shader.inputs[2]
    nodelinks.new(node_out, node_in)

    #add material output node  and connect mix_shader output
    output = matnodes.new('ShaderNodeOutputMaterial')
    node_out = mix_shader.outputs[-1]
    node_in = output.inputs[0]
    nodelinks.new(node_out, node_in)
    obj.data.materials.append(material)
    return material

def add_solar_dynamics(sun):
    #add forcefield
    bpy.ops.object.effector_add(type='FORCE', radius=sun.equaRadius+(sun.equaRadius*0.1), enter_editmode=False, location=(0, 0, 0))
    forcefield = bpy.data.objects['Field']
    forcefield.name = 'SolarField'
    forcefield.field.flow = 1.
    forcefield.field.strength = 20.
    forcefield.field.noise = 1.
    #sun object
    name = sun.englishName 
    obj = select_object(name)
    bpy.ops.object.modifier_add(type='SMOKE')
    #bpy.ops.object.material_slot_add()
    bpy.ops.object.quick_smoke()
    #bpy.ops.object.quick_fluid()
    # get smokemodifier on object
    obj.display_type = 'SOLID'
    objmod = obj.modifiers['Smoke']
    objmod.flow_settings.smoke_flow_type = 'FIRE'
    objmod.flow_settings.surface_distance = 10 

    #configure smoke domain
    smokedomain = bpy.data.objects['Smoke Domain']
    smokedomain.name = 'SolarDomain'
    smokemod = smokedomain.modifiers['Smoke']

    smokemod.domain_settings.beta = 0
    smokemod.domain_settings.resolution_max = 128
    smokemod.domain_settings.use_high_resolution = True

    #settings for smoke domain Texture 
    mat = list(smokedomain.data.materials)[0]
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    pvolume = nodes['Principled Volume']
    pvolume.inputs[7].default_value = (1, 0.2955, 0.02533, 1) #bpy_prop_array
    pvolume.inputs[2].default_value = 0.
    pvolume.inputs[8].default_value = 1. 
    pvolume.inputs[10].default_value = 800. #blackbody intensity
    #smokemod smoke domain 

    # attribute and emission
    attr = nodes.new('ShaderNodeAttribute')
    attr.attribute_name = 'Flames'
    nout = attr.outputs[2] 
    nmath = nodes.new('ShaderNodeMath')
    nmath.operation = 'MULTIPLY'
    nmath.inputs[1].default_value = 15.
    nin = nmath.inputs[0]
    links.new(nout, nin)
    nout = nmath.outputs[0]
    nin = pvolume.inputs[6]
    links.new(nout, nin)
    return obj, forcefield, smokedomain



def add_texture(planet, texture):
    name = planet.englishName
    #setup image(s)
    #base color 
    base_img_path = texture.textures[name]['albedo']
    bpy.data.images.load(base_img_path, check_existing=False)
    base_img = bpy.data.images[f"{os.path.basename(base_img_path)}"]
    base_img.name = f"{planet.englishName}_albedo"
    base_img.colorspace_settings.name = 'sRGB'
    base_img.source = 'FILE'
    base_img.filepath = base_img_path

    #bpy.ops.image.open(filepath=base_img_path, directory=os.path.dirname(base_img_path), files=[{"name": f"{os.path.basename(base_img_path)}"}], relative_path=False, show_multiview=False) 
    #bpy.data.images[f"{os.path.basename(base_img_path)}"].colorspace_settings.name = 'sRGB'
    #bpy.data.images[f"{os.path.basename(base_img_path)}"].source = 'FILE'
    #bpy.data.images[f"{os.path.basename(base_img_path)}"].filepath = base_img_path
    #normal map 
    normal_img_path = texture.textures[name]['normal']
    bpy.data.images.load(normal_img_path, check_existing=False)
    normal_img = bpy.data.images[f"{os.path.basename(normal_img_path)}"]
    normal_img.name = f"{planet.englishName}_normal"
    normal_img.colorspace_settings.name = 'Non-Color'
    normal_img.source = 'FILE'
    normal_img.filepath = normal_img_path


    #bpy.ops.image.open(filepath=normal_img_path, directory=os.path.dirname(normal_img_path), files=[{"name": f"{os.path.basename(normal_img_path)}"}], relative_path=False, show_multiview=False) 
    #bpy.data.images[f"{os.path.basename(normal_img_path)}"].colorspace_settings.name = 'Non-Color'
    #print(bpy.data.images[f"{os.path.basename(normal_img_path)}"].colorspace_settings.name)
    #bpy.data.images[f"{os.path.basename(normal_img_path)}"].source = 'FILE'
    #bpy.data.images[f"{os.path.basename(normal_img_path)}"].filepath = normal_img_path
    #spec map 
    spec_img_path = texture.textures[name]['specular']
    bpy.data.images.load(spec_img_path, check_existing=False)
    spec_img = bpy.data.images[f"{os.path.basename(spec_img_path)}"]
    spec_img.name = f"{planet.englishName}_specular"
    spec_img.colorspace_settings.name = 'Non-Color'
    spec_img.source = 'FILE'
    spec_img.filepath = spec_img_path


    # bpy.ops.image.open(filepath=spec_img_path, directory=os.path.dirname(spec_img_path), files=[{"name": f"{os.path.basename(spec_img_path)}"}], relative_path=False, show_multiview=False) 
    #bpy.data.images[f"{os.path.basename(spec_img_path)}"].colorspace_settings.name = 'Non-Color'
    #print(bpy.data.images[f"{os.path.basename(spec_img_path)}"].colorspace_settings.name)
    #bpy.data.images[f"{os.path.basename(spec_img_path)}"].source = 'FILE'
    #bpy.data.images[f"{os.path.basename(spec_img_path)}"].filepath = spec_img_path


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
    #image_texture.image = bpy.data.images.load( bpy.data.images[f"{os.path.basename(base_img_path)}"].filepath , check_existing=True)
    image_texture.image = bpy.data.images.load( bpy.data.images[f"{obj.name}_albedo"].filepath, check_existing=True) 
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

    #add normal map, link normal map from mapping to texture_image and then from tex_image, to bsdg
    normal_texture = matnodes.new('ShaderNodeTexImage')
    #normal_texture.image = bpy.data.images.load( bpy.data.images[f"{os.path.basename(normal_img_path)}"].filepath , check_existing=True)
    normal_texture.image = bpy.data.images.load( bpy.data.images[f"{obj.name}_normal"].filepath, check_existing=True) 
    normal_texture.interpolation = 'Cubic'
    normal_texture.projection = 'SPHERE'
    normal_texture.extension = 'EXTEND'
    # connect mapping to image texture
    node_out = mapping.outputs[-1]
    node_in = normal_texture.inputs[-1]
    nodelinks.new(node_out, node_in)
    # connect image texture to BSDF normal input
    node_out = normal_texture.outputs[0]
    node_in = bsdf_shader.inputs[19]
    nodelinks.new(node_out, node_in)

    #add spec map. link spec map from mappng to texture_image and then from teximage to bsdf 
    spec_texture = matnodes.new('ShaderNodeTexImage')
    #spec_texture.image = bpy.data.images.load( bpy.data.images[f"{os.path.basename(spec_img_path)}"].filepath , check_existing=True)
    spec_texture.image = bpy.data.images.load( bpy.data.images[f"{obj.name}_specular"].filepath, check_existing=True) 
    spec_texture.interpolation = 'Cubic'
    spec_texture.projection = 'SPHERE'
    spec_texture.extension = 'EXTEND'
    #connect mapping to image texture
    node_out = mapping.outputs[-1]
    node_in = spec_texture.inputs[-1]
    nodelinks.new(node_out, node_in)
    # connect image texture to BSDF spectral input
    node_out = spec_texture.outputs[0]
    node_in = bsdf_shader.inputs[5]
    nodelinks.new(node_out, node_in)

    obj.data.materials.append(material)
    return material






