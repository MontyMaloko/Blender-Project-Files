bl_info = {
    "name": "Material Checker",
    "author": "Jacine",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool",
    "description": "Check if any materials contain 'Material' in their name and isolate those objects",
    "category": "Material",
}

import bpy

class OBJECT_OT_check_material_names(bpy.types.Operator):
    bl_idname = "object.check_material_names"
    bl_label = "Check Material Names and Isolate"
    bl_description = "Check if any materials contain 'Material' in their name and isolate flagged objects"

    def execute(self, context):
        search_term = "Material"
        materials_with_default_name = []
        objects_to_isolate = []

        # Get the active view layer
        view_layer = context.view_layer

        # Loop through all objects in the scene
        for obj in bpy.data.objects:
            # Check if the object is in the active view layer and is visible
            if obj.visible_get() and obj.type == 'MESH' and obj.data.materials:
                for mat in obj.data.materials:
                    # Check if 'Material' is part of the material name
                    if mat and search_term in mat.name:
                        materials_with_default_name.append((mat.name, obj.name))
                        objects_to_isolate.append(obj)  # Collect objects to isolate

        if materials_with_default_name:
            # Create a report message by joining material and object names
            report_msg = "Found materials named 'Material':\n"
            for mat_name, obj_name in materials_with_default_name:
                report_msg += f"Material: {mat_name} on Object: {obj_name}\n"

            # Check character limit of self.report and adjust message accordingly
            if len(report_msg) > 256:
                report_msg = "Found materials named 'Material'. See system console for details."
                print(report_msg)  # Log the full message in the console
            else:
                self.report({'INFO'}, report_msg.strip())

            # Isolate flagged objects
            if objects_to_isolate:
                # Deselect all objects first
                bpy.ops.object.select_all(action='DESELECT')
                
                # Select the objects to isolate
                for obj in objects_to_isolate:
                    if obj.visible_get():  # Ensure the object is visible in the view layer
                        obj.select_set(True)
                        context.view_layer.objects.active = obj

                # Switch to Local View (isolate mode)
                bpy.ops.view3d.localview()

        else:
            self.report({'INFO'}, "No unnamed materials found.")
        
        return {'FINISHED'}

class VIEW3D_PT_material_name_checker(bpy.types.Panel):
    bl_label = "Material Name Checker"
    bl_idname = "VIEW3D_PT_material_name_checker"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.check_material_names")

# Register and Unregister functions
def register():
    bpy.utils.register_class(OBJECT_OT_check_material_names)
    bpy.utils.register_class(VIEW3D_PT_material_name_checker)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_check_material_names)
    bpy.utils.unregister_class(VIEW3D_PT_material_name_checker)

if __name__ == "__main__":
    register()
