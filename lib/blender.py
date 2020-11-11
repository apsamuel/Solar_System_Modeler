import os, sys
sys.path.extend([os.path.join('.', 'lib')])


#import orbital
import bpy 
import math




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

def normalized_frame(mini= 0.0, maxi = math.pi*2):
    """
    mini: float (Min. value for normalize frame)
    maxi: float (Max. value for normalize frame)
    Returns normalized value for current frame between `mini` and `maxi` values
    """
    mini = float(mini)
    maxi = float(maxi)
    frame = float(bpy.context.scene.frame_current)
    print(f"frame value: {frame}")
    # use standard normalization function with frame values
    print(f"({maxi} - {mini}) * ({frame} - {mini}) / (float(frames()) - 1.00) + {mini}")
    return float(
        (maxi - mini) * (frame - mini) / (float(frames()) - float(1)) + mini
    )

# helper methods for calculating positions, angles, and other things between objects in a blender scene
def get_angle_a(a,b,c):
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

def get_angle_b(a,b,c):
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

def get_angle_c(a,b,c):
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

def select_object(name):
    """
    name: str (blender object name)
    Selects and Returns requested object if exists
    """
    obj = bpy.context.scene.objects[name]
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj 
    obj.select_set(True)
    return obj

def scene_props(sys_u ='METRIC', len_u ='KILOMETERS', mass_u ='KILOGRAMS', seperate_u= True, scale_u = 100000.00, grid_scale = 100000.00, f_len = 50.0, c_start = 100.00, c_end = 100000.00):
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

    for workspace in list(bpy.data.workspaces):
        print(f"workspace: {workspace.name}")
        screens = list(workspace.screens)
        for screen in screens:
            print(f"screen: {screen.name}")
            areas = list(screen.areas)
            for area in areas:
                spaces = area.spaces
                for space in spaces:
                    print(f"space type: {space.type}")
                    if space.type == "VIEW_3D":
                        space.overlay.grid_scale = scale_u 
                        space.overlay.show_axis_x = True 
                        space.overlay.show_axis_y = True
                        space.overlay.show_axis_z = True  
                        space.overlay.show_floor = True
                        space.overlay.show_ortho_grid = True
                        space.lens = f_len 
                        space.clip_start = c_start 
                        space.clip_end = c_end 

def refresh_panels(space_type = "PROPERTIES", region_type ="WINDOW"):
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

def insert_custom_attributes(name, planet):
    """
    name: str (name of blender object to attach attributes to, note: works for MESH and EMPTY objects currently)
    planet: Planet (pass in the Planet object)
    adds custom attributes from python planet object object to corresponding blender object (parent Empty by default)
    """
    obj = select_object(name)
    print(f"working with: {obj.name}")
    for i in planet.keys: 
        if obj.type == 'MESH':
            obj.data[i] = planet.__getattribute__(i)
        else:
            obj[i] = planet.__getattribute__(i) 

    refresh_panels()

def add_orbital_drivers(name, planet):
    """
    name: str (name of blender object to attach orbital drivers to, note: this should be a planets parent object and correspond to the python object, by default attached to an EMPTY)
    planet: Planet (pass in the Planet object)
    adds motion drivers (x tranlation, y tranlation, z rotation) to parent empty object for planet
    """
    planetPrimitive = select_object(name)
    xdriver = planetPrimitive.driver_add("location", 0).driver
    ydriver = planetPrimitive.driver_add("location", 1).driver
    zdriver = planetPrimitive.driver_add("rotation_euler", 2).driver 
    # x motion driver vars
    semi_major_axis = xdriver.variables.new()
    semi_major_axis.name = "semi_major_axis"
    semi_major_axis.targets[0].id = planetPrimitive
    semi_major_axis.targets[0].data_path = '["semimajorAxis"]'
    # y motion driver vars
    semi_minor_axis = ydriver.variables.new()
    semi_minor_axis.name = "semi_minor_axis"
    semi_minor_axis.targets[0].id = planetPrimitive 
    semi_minor_axis.targets[0].data_path = '["semiminorAxis"]'
    # z motion driver vars
    sideral_rot = zdriver.variables.new()
    sideral_rot.name = "sideral_rot"
    sideral_rot.targets[0].id = planetPrimitive
    sideral_rot.targets[0].data_path = '["sideralRotation"]'
    # (x,y,z) motion driver expressions
    #xdriver.expression = f"(semi_major_axis*(cos(frame/80)))+0"
    #ydriver.expression = f"(semi_minor_axis*(sin(frame/80)))+0"
    # use normalized frame function defaulted to a range of 0-2(pi)
    xdriver.expression = f"(semi_major_axis*(cos(normalized_frame())))+0"
    ydriver.expression = f"(semi_minor_axis*(sin(normalized_frame())))+0"    
    zdriver.expression = f"(360/sideral_rot)*frame"
    return planetPrimitive


def primitive_natural_satellites_add(planet, sub_divisions = 100):
    """
    planet: Planet (pass in Planet object)
    sub_divisions: float ()
    adds known natural satellites, an orbital path for each, and adds follow path constraint to satellite object, each object is parented to it's owning planets empty
    NOTE: The follow path constraint is used for orbital motion 
    TODO:  z-euler rotation driver for axial rotation
    """
    moons = planet.moonData  
    for moon in moons:
        print(f"original: {moon.englishName} semiminor: {moon.semiminorAxis} semimajor: {moon.semimajorAxis} equaRadius: {moon.equaRadius}")
        moon.scale_moon()
        print(f"scaled: {moon.englishName} semiminor: {moon.semiminorAxis} semimajor: {moon.semimajorAxis} equaRadius: {moon.equaRadius}")
        print(f"x equation: {moon.semimajorAxis}*(cos(u)*cos(v))")
        print(f"y equation: {moon.semiminorAxis}*(cos(u)*sin(v))")
        bpy.ops.mesh.primitive_xyz_function_surface(x_eq=f"{moon.semimajorAxis}*(cos(u)*cos(v))", y_eq=f"{moon.semiminorAxis}*(cos(u)*sin(v))", z_eq="0", wrap_u=False, range_v_max=12.5664, close_v=False)
        moonOrbitalPath = bpy.context.active_object
        moonOrbitalPath.name = f"Orbital_Path_{moon.englishName}"
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
        moonObject.parent = bpy.data.objects[f"empty_{planet.englishName}"]
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        moonObject.constraints["Follow Path"].target = bpy.data.objects[f"Orbital_Path_{moon.englishName}"]
        moonObject.constraints["Follow Path"].use_curve_follow = True 
        moonObject.constraints["Follow Path"].forward_axis = 'FORWARD_Y'
        moonObject.constraints["Follow Path"].influence = 0.215
        bpy.data.curves[f"Orbital_Path_{moon.englishName}"].path_duration = frames()
       # moonOrbitalPath.motion_path.frame_start = 1
       # moonOrbitalPath.motion_path.frame_end = frames()
        #select_object(f"Key_{moon.englishName}")
        override={'constraint':moonObject.constraints["Follow Path"]}
        bpy.ops.constraint.followpath_path_animate(override,constraint="Follow Path", owner='OBJECT')



# Planet 'Primitive'
def primitive_planet_add(planet, sub_divisions=100):
    """
    planet: Planet (pass in Planet object)
    sub_divisions: float (the number of subdivisions for plane primitive, more divisions for higher quality, but slower render)
    adds planet to scene at origin
    NOTE: should call Planet.scale_planet() first 
    TODO:  z-euler rotation driver for axial rotation
    """
    diameter = planet.equaRadius*2
    obj_name = planet.englishName
    rot_global_radians = float(format(math.radians(90), '.4f'))
    bpy.ops.mesh.primitive_plane_add(size=diameter, enter_editmode=False, location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.name = obj_name
    plane.data.name = f"mesh_{obj_name}"
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
    empty.name = f"empty_{obj_name}"
    plane.parent = empty
    insert_custom_attributes(f"empty_{obj_name}", planet)

