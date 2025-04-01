bl_info = {
    "name": "Auto Renamer",
    "blender": (2, 82, 0),  # Adjust according to your Blender version
    "category": "Object",
    "description": "Automatically renames materials, meshes, objects, cameras, curves, empties, and lights with specified prefixes.",
    "author": "Jacine",
    "version": (1, 1),
    "support": "COMMUNITY",
}

import bpy
import threading

# Function to rename objects and materials
def rename_objects_and_materials(scene):
    for obj in scene.objects:
        if obj.type == 'MESH' and not obj.name.startswith("GEO_"):
            obj.name = "GEO_" + obj.name
            if obj.data and not obj.data.name.startswith("GEO_"):
                obj.data.name = "GEO_" + obj.data.name
        
        if obj.type == 'CAMERA' and not obj.name.startswith("CAM_"):
            obj.name = "CAM_" + obj.name
        
        if obj.type == 'CURVE' and not obj.name.startswith("CRV_"):
            obj.name = "CRV_" + obj.name
        
        if obj.type == 'EMPTY' and not obj.name.startswith("NULL_"):
            obj.name = "NULL_" + obj.name
        
        if obj.type in {'LIGHT', 'LAMP'} and not obj.name.startswith("LGT_"):
            obj.name = "LGT_" + obj.name

    for mat in bpy.data.materials:
        if not mat.name.startswith("MTL_"):
            mat.name = "MTL_" + mat.name

    print("Renaming operation completed.")

# Define the operator for manual execution
class OBJECT_OT_rename_handler(bpy.types.Operator):
    bl_idname = "object.rename_handler"
    bl_label = "Rename Objects and Materials"
    bl_description = "Automatically rename objects and materials with appropriate prefixes"

    def execute(self, context):
        rename_objects_and_materials(context.scene)
        return {'FINISHED'}

# Define the panel where the button will appear
class VIEW3D_PT_auto_rename(bpy.types.Panel):
    bl_label = "Auto Renamer"
    bl_idname = "VIEW3D_PT_auto_rename"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.rename_handler")

# Timer callback function
def timer_callback():
    scene = bpy.context.scene
    rename_objects_and_materials(scene)
    return 30.0  # Adjust the interval (in seconds) to control the frequency of checks

# Handler function to trigger on new scene creation or file load
def on_scene_update(scene):
    rename_objects_and_materials(scene)

# Register the operator, panel, and handlers
def register():
    bpy.utils.register_class(OBJECT_OT_rename_handler)
    bpy.utils.register_class(VIEW3D_PT_auto_rename)
    
    # Handlers to run the function when Blender loads, or a new scene is created
    bpy.app.handlers.load_post.append(on_scene_update)
    bpy.app.handlers.depsgraph_update_post.append(on_scene_update)
    
    # Timer function to run periodically
    bpy.app.timers.register(timer_callback)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_rename_handler)
    bpy.utils.unregister_class(VIEW3D_PT_auto_rename)
    
    # Remove handlers and stop the timer
    bpy.app.handlers.load_post.remove(on_scene_update)
    bpy.app.handlers.depsgraph_update_post.remove(on_scene_update)
    bpy.app.timers.unregister(timer_callback)

if __name__ == "__main__":
    register()