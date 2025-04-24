# Maya code to populate a mesh (.obj) with cubes

# --------------------------------------------------------------------
# This code does not generate the final mesh for the project, because unfortunately, I cannot create cubes smaller than 0.5 in size without causing Maya to crash.
# Additionally, due to the angle at which the head needs to be shown to create the illusion, the head was not perceptible with the cubes that I can process using this code.
# However, I decided to include this code because part of the process of creating something new involves testing and changing approaches.
# The code works well for generating the voxel cubes in any obj file.
# --------------------------------------------------------------------

# References----------------------------------------------------------
# https://download.autodesk.com/us/maya/2009help/CommandsPython/intersect.html
# https://download.autodesk.com/us/maya/2011help/api/class_m_fn_mesh.html
# https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=Maya_SDK_Maya_Python_API_Maya_Python_API_1_0_Using_the_Maya_Python_API_html
# --------------------------------------------------------------------

# Import the Maya libraries
import maya.cmds as cmds
import maya.api.OpenMaya as om 

# Create and array to store the origin of all the cubes in the voxel grid.
voxel_cube_origins = om.MPointArray()

def import_model (filepath):
    """Imports the obj model into maya given a file path."""
    imported_nodes = cmds.file(filepath, i = True, type = "OBJ", options = "mo=1", returnNewNodes = True)
    return imported_nodes

def scale_model(model, scalar):
    cmds.scale(scalar ,scalar ,scalar, model)
    
def move_relative(model, position):
    cmds.move( position[0] , position[1], position[2], model, absolute = True)

# Created with ChatGPT --------------
def align_with_floor(model):
    """Helps to allign assets on the floor."""
    
    # Step 1: Get the bounding box values
    bounding_box = cmds.exactWorldBoundingBox(model)

    # Step 2: Move the model so that its bottom is at y = 0
    cmds.move(0, -bounding_box[1], 0, model)  # Move up so bottom aligns to 0
# -----------------------------------------

def get_width (model):
    bounding_box = cmds.exactWorldBoundingBox(model)
    return bounding_box[3] - bounding_box[0]

def get_height (model):
    bounding_box = cmds.exactWorldBoundingBox(model)
    return bounding_box[4] - bounding_box[1]

def get_depth (model):
    bounding_box = cmds.exactWorldBoundingBox(model)
    return bounding_box[5] - bounding_box[2]

def voxel_grid(width, heigth, depth, scale):
    """This function creates the origin positions for all the cubes in the voxel grid. The grid is defined based on the bounding box dimensions of the mesh."""
    num_cubes_width = round(width / scale)
    num_cubes_height = round(heigth / scale)
    num_cubes_depth =  round(depth / scale)

    offset_x = (num_cubes_width * scale)/2
    offset_z = (num_cubes_depth * scale)/2

    for x in range(num_cubes_width):
        for y in range(num_cubes_height):
            for z in range(num_cubes_depth):
                position_x = ((x * scale) - offset_x)
                position_y = (y * scale)
                position_z = ((z * scale) - offset_z)
                voxel_cube_origins.append(om.MPoint(position_x,position_y,position_z))    
    return voxel_cube_origins 

def get_mesh_fn(model):
    """Get the data(vertices) """
    selection_list = om.MSelectionList()
    shape_node = model[1]
    selection_list.add(shape_node)
    dag_path = selection_list.getDagPath(0)
    mesh_fn = om.MFnMesh(dag_path)
    return mesh_fn

def test_if_point_is_inside_mesh(mesh, point, direction):
    """This function uses the anyIntersection function available on maya to test if the point is inside or outside the mesh"""
    raySource = om.MFloatPoint(point)
    rayDirection = om.MFloatVector(direction)
    rayDirection.normalize()  # Normalize the direction vector

    space = om.MSpace.kWorld  # Using world space
    maxParam = 1000.0  # Maximum distance for the search
    testBothDirections = False  # Search only in the ray's direction

    # Perform intersection with ray tracing function
    intersection_result = mesh.anyIntersection(
        raySource, rayDirection, space, maxParam, testBothDirections
    )
    validation = intersection_validation(intersection_result)
    return validation


# Extracted from ChatGPT --------------
def intersection_validation( intersection_result):
    if intersection_result:  # Check if intersection_result is not None
        hitPoint, hitRayParam, hitFace, hitTriangle, hitBary1, hitBary2 = intersection_result

        # If hitRayParam is greater than zero, the intersection happened
        if hitRayParam > 0:
            return True  # Point is inside the mesh (intersection occurred)
    
    return False  # No intersection or point is outside the mesh
# --------------------------------------

def filter_points_by_ray_intersection_direction(mesh, array_with_voxel_origins, direction):
    """Filter cubes by ray intersection along the n direction."""
    remaining_cubes = []
    for point in array_with_voxel_origins:
        if test_if_point_is_inside_mesh(mesh, point, direction):
            remaining_cubes.append(point)
    return remaining_cubes

def classify_points_by_ray_intersections(mesh, array_with_voxel_origins):
    """Classify the points by applying ray tests sequentially on the X, Y, Z  and other auxiliary directions."""
    # Note: I took this approach because testing the intersection in just one direction does not properly identify cubes inside the mesh.
    
    # Step 1: Filter by X-axis
    direction_x = (1.0, 0.0, 0.0)
    filtered_by_x = filter_points_by_ray_intersection_direction(mesh, array_with_voxel_origins, direction_x)
    
    # Step 2: Filter by Y-axis (on the remaining cubes)
    direction_y = (0.0, 1.0, 0.0)
    filtered_by_y = filter_points_by_ray_intersection_direction(mesh, filtered_by_x, direction_y)
    
    # Step 3: Filter by Z-axis (on the remaining cubes)
    direction_z = (0.0, 0.0, 1.0)
    filtered_by_z = filter_points_by_ray_intersection_direction(mesh, filtered_by_y, direction_z)

    # Step 4: Filter by diagonal-1
    direction_diagonal_1 = (1.0, 1.0, 0.0)
    final_filter_1 = filter_points_by_ray_intersection_direction(mesh, filtered_by_z, direction_diagonal_1)

    # Step 5: Filter by diagonal-2
    direction_diagonal_2 = (-1.0, 1.0, 0.0)
    
    # The remaining cubes after all filtering steps
    final_filter = filter_points_by_ray_intersection_direction(mesh, final_filter_1, direction_diagonal_2)
    
    return final_filter

def draw_cube(pos_x, pos_y, pos_z, scale):
    cube = cmds.polyCube (w = scale, h = scale, d = scale)
    cmds.move(pos_x, pos_y, pos_z ,cube)

def display_final_mesh(cubes_inside_mesh, scale):
    for point in cubes_inside_mesh:
        draw_cube(point.x, point.y, point.z, scale)

def main():
    # Make sure the filepath of the .obj file is correct to avoid issues in the MayaScript editor
    # filepath = '/absolute/path/to/file/head_1.obj'    
    filepath = '/home/s5628585/Maya_Final_Project/assets/head_1.obj' # My route

    model = import_model(filepath)

    # Scale the model
    scale_model(model, 80) 

    # Align model to the floor
    align_with_floor(model)

    # Cube size (smaller cube sizes provide better resolution. Unfortunately, I cannot generate cubes smaller than a 0.5 scale value in Maya!)
    scale = 1 

    # Model width, height and depth
    model_width = get_width(model)
    model_height =  get_height(model)
    model_depth = get_depth (model)

    # Creating the origin positions for all the cubes in the voxel grid. These positions will later be used as the starting points for ray tracing intersection.
    voxel_grid(model_width, model_height, model_depth, scale)

    # Get the right mesh type to be processed
    mesh = get_mesh_fn(model)
    
    # Indentifing the cubes that are inside the mesh    
    cubes_inside = classify_points_by_ray_intersections(mesh, voxel_cube_origins )

    # Display the final mesh with cubes
    display_final_mesh(cubes_inside , scale)

if __name__ == "__main__":
    main()
