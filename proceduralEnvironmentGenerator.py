def add_shrinkwrap(data, target):
    """
    Adds a shrinkwrap constraint to the given data object, constraining it to the given target object.

    Args:
        data (bpy_prop_collection): The data collection to which the constraint will be added.
        target (bpy_object): The target object to which the data object will be constrained.

    Returns:
        bpy_object: The newly created shrinkwrap constraint.
    """
    con = data.constraints.new("SHRINKWRAP")
    con.target = target
    con.shrinkwrap_type = "PROJECT"
    con.project_axis = "NEG_Z"
    return con


def lookAt(obj, target):
    """
    Orients the given object so that it is looking at the given target location.

    Args:
        obj (bpy_object): The object to be oriented.
        target (list): The target location, given as a list of X, Y, and Z coordinates.

    Returns:
        None: The object's rotation is modified in-place.
    """
    position = mathutils.Vector((obj.location[0], obj.location[1], obj.location[2]))
    target_position = mathutils.Vector((target[0], target[1], target[2]))
    default_direction = mathutils.Vector((0, -1, 0))

    direction = (target_position - position).normalized()
    angle = math.acos(default_direction.dot(direction))

    rotation = default_direction.cross(direction).normalized()
    obj.delta_rotation_euler = [0, 0, rotation[2] * angle]


def random_direction(obj):
    """
    Randomly rotates the given object by a random angle around its Z axis.

    Args:
        obj (bpy_object): The object to be rotated.

    Returns:
        None: The object's rotation is modified in-place.
    """
    obj.delta_rotation_euler = [0, 0, random.uniform(0, math.pi * 2)]


def increase_random_size(obj):
    """
    Randomly increases the size of the given object by a small amount.

    Args:
        obj (bpy_object): The object to be resized.

    Returns:
        None: The object's scale is modified in-place.
    """
    val = random.random() / 1.5
    obj.delta_scale = [obj.delta_scale[0] + val, obj.delta_scale[1] + val, obj.delta_scale[2] + val]


def add_material(obj, color):
    """
    Adds a new material to the given object, with the given diffuse color.

    Args:
        obj (bpy_object): The object to which the material will be applied.
        color (list): The diffuse color of the material, given as a list of R, G, B, and A values between 0 and 1.

    Returns:
        bpy_material: The newly created material.
    """
    mat = bpy.data.materials.new(name="Material")
    mat.diffuse_color = color
    mat.specular_intensity = 0
    mat.roughness = 1
    obj.data.materials.append(mat)
    return mat


def isNearObjects(obj, arr, min_distance):
    """
    Returns True if the given object is within a certain distance of any of the given objects, False otherwise.

    Args:
        obj (list): The object's location, given as a list of X, Y, and Z coordinates.
        arr (list): The list of objects to be checked.
        min_distance (float): The minimum distance between the object and an object in the list for the check to succeed.

    Returns:
        bool: True if the object is within min_distance of any object in the list, False otherwise.
    """
    position = mathutils.Vector((obj[0], obj[1], obj[2]))
    result = False
    for i in arr:
        if not result:
            target_position = mathutils.Vector((i[0], i[1], i[2]))
            direction = (target_position - position)
            distance = math.sqrt(math.pow(direction.x, 2) + math.pow(direction.y, 2))
            if min_distance >= distance:
                result = True
    return result


# -----------------------------------
# Forest
# -----------------------------------

# two parameters are defined, beta_a and beta_b, which are used to control the distribution of the random points 
# that will be used to place the trees in the forest. The forest_size parameter defines the number of points to generate, 
# and the forest_scale parameter controls the size of the trees.

# The code then generates a random array of points using the np.random.default_rng().beta() function, 
# which generates forest_size points from a beta distribution with parameters beta_a and beta_b. 
# The points are then scaled by forest_scale and shifted by -forest_size/2 to center them on the plane.

# The code then loops through each point in the array, 
# checking if it is within a certain distance (3 units) of any other point in the used_positions array. 
# If the point is not near any other points, it is copied to a new object, 
# its location is set to the current point, and it is added to the collection. 
# The object is then constrained to the plane, rotated randomly, scaled randomly, and added to the used_positions array.

# This code demonstrates how to generate a random array of points from a beta distribution, 
# how to check if a point is near another point, and how to generate and add new objects to a Blender scene.


beta_a = 1
beta_b = 1

forest_size = 80

forest_scale = 120


beta_random = (np.random.default_rng().beta(beta_a ,beta_b,  size=(forest_size,2)) * forest_scale) - forest_size / 2

trees = []
with bpy.data.libraries.load(r"D:\meOneD\OneDrive\_comps\_Blender\_MyBlender\Blender_pythonScenes\BlenderNumpy_VillageScript\assets\tree_01.blend") as (data_from, data_to):
    data_to.objects.append(data_from.objects[0])
trees.append(data_to.objects[0])
with bpy.data.libraries.load(r"D:\meOneD\OneDrive\_comps\_Blender\_MyBlender\Blender_pythonScenes\BlenderNumpy_VillageScript\assets\tree_02.blend") as (data_from, data_to):
    data_to.objects.append(data_from.objects[0])
trees.append(data_to.objects[0])
with bpy.data.libraries.load(r"D:\meOneD\OneDrive\_comps\_Blender\_MyBlender\Blender_pythonScenes\BlenderNumpy_VillageScript\assets\tree_03.blend") as (data_from, data_to):
    data_to.objects.append(data_from.objects[0])
trees.append(data_to.objects[0])
with bpy.data.libraries.load(r"D:\meOneD\OneDrive\_comps\_Blender\_MyBlender\Blender_pythonScenes\BlenderNumpy_VillageScript\assets\tree_04.blend") as (data_from, data_to):
    data_to.objects.append(data_from.objects[0])
trees.append(data_to.objects[0])
with bpy.data.libraries.load(r"D:\meOneD\OneDrive\_comps\_Blender\_MyBlender\Blender_pythonScenes\BlenderNumpy_VillageScript\assets\tree_05.blend") as (data_from, data_to):
    data_to.objects.append(data_from.objects[0])
trees.append(data_to.objects[0])

for i in np.unique(beta_random,axis=0):
    if not isNearObjects([i[0], i[1], 3],used_positions,3):
        obj = trees[random.randint(0,len(trees)-1)].copy()
        obj.location = (i[0], i[1], 3)
        col.objects.link(obj)
        add_shrinkwrap(obj,plane_obj)
        random_direction(obj)
        increase_random_size(obj)
        used_positions.append([i[0], i[1], 3])




# -----------------------------------
# Village
# -----------------------------------


town_size = 30
town_scale = 30


town_position_x = 3
town_position_y = 3

town_t = np.linspace(0, (2*np.pi / size) * (size - 1), size)
town_formula_x = ((town_scale * np.cos(town_t)) + town_position_x)[:, np.newaxis]
town_formula_y = ((town_scale * np.sin(town_t)) + town_position_y)[:, np.newaxis]

town_coor_set = np.hstack((town_formula_x,town_formula_y))


houses = []
with bpy.data.libraries.load(r"D:\meOneD\OneDrive\_comps\_Blender\_MyBlender\Blender_pythonScenes\BlenderNumpy_VillageScript\assets\house_01.blend") as (data_from, data_to):
    data_to.objects.append(data_from.objects[0])
houses.append(data_to.objects[0])
with bpy.data.libraries.load(r"D:\meOneD\OneDrive\_comps\_Blender\_MyBlender\Blender_pythonScenes\BlenderNumpy_VillageScript\assets\house_02.blend") as (data_from, data_to):
    data_to.objects.append(data_from.objects[0])
houses.append(data_to.objects[0])
with bpy.data.libraries.load(r"D:\meOneD\OneDrive\_comps\_Blender\_MyBlender\Blender_pythonScenes\BlenderNumpy_VillageScript\assets\house_03.blend") as (data_from, data_to):
    data_to.objects.append(data_from.objects[0])
houses.append(data_to.objects[0])

for i in np.unique(town_coor_set,axis=0):
    obj_position = mathutils.Vector((i[0], i[1], 4))
    center_position = mathutils.Vector((town_position_x, town_position_y, 4))
    direction = (obj_position - center_position).normalized() * random.randint(-1,5)
    obj_position = obj_position + direction
    if not isNearObjects([obj_position[0], obj_position[1], 4],used_positions,3):
        obj = houses[random.randint(0,len(houses)-1)].copy()
        obj.location = (obj_position[0], obj_position[1], 4)
        col.objects.link(obj)
        add_shrinkwrap(obj,plane_obj)
        lookAt(obj,[town_position_x, town_position_y, 4])
        used_positions.append([obj_position[0], obj_position[1], 4])
