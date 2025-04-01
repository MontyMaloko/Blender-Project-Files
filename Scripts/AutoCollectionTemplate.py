bl_info = {
    "name": "Auto Create Collections",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Jacine",
}

import bpy

# Define the main collections and their sub-collections
collections_hierarchy = {
    "Archive": [],
    "Model": ["High Poly", "Low Poly"],
    "Reference": ["Base"],
    "Render Objects": [],
    "Rig": [],
    "Sculpt": ["Backup"],
    "Simulation": []
}

# Function to create a collection if it doesn't already exist
def create_collection(name, parent=None):
    if name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(name)
        if parent:
            parent.children.link(new_collection)
        else:
            bpy.context.scene.collection.children.link(new_collection)
        print(f"Collection '{name}' created under '{parent.name if parent else 'Scene Collection'}'.")
        return new_collection
    else:
        print(f"Collection '{name}' already exists.")
        return bpy.data.collections[name]

# Function to delete the default "Collection" collection
def delete_default_collection():
    default_name = "Collection"
    if default_name in bpy.data.collections:
        default_collection = bpy.data.collections[default_name]
        bpy.context.scene.collection.children.unlink(default_collection)
        bpy.data.collections.remove(default_collection)
        print(f"Default collection '{default_name}' deleted.")
    else:
        print(f"Default collection '{default_name}' does not exist or has already been deleted.")

# Create the collections and their sub-collections, then delete the default collection
def create_collections():
    # Make sure this is run only in the correct context
    if bpy.context.scene:
        for parent_name, children in collections_hierarchy.items():
            parent_collection = create_collection(parent_name)
            for child_name in children:
                create_collection(child_name, parent_collection)
        delete_default_collection()
        print("Collection creation process complete.")

# Define the operator
class OBJECT_OT_create_collections(bpy.types.Operator):
    bl_idname = "object.create_collections"
    bl_label = "Collection Template"
    bl_description = "Create predefined collections and their sub-collections if they do not already exist"
    
    def execute(self, context):
        create_collections()
        return {'FINISHED'}

# Define the panel where the button will appear
class VIEW3D_PT_collection_template(bpy.types.Panel):
    bl_label = "Collection Template"
    bl_idname = "VIEW3D_PT_collection_template_unique"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Collections'  # Changed to 'Collections' to avoid conflict with other tabs

    def draw(self, context):
        layout = self.layout
        layout.operator("object.create_collections")

# Handler function to trigger on new scene creation or file load
def on_scene_update(scene):
    create_collections()

# Register the operator, panel, and handlers
def register():
    bpy.utils.register_class(OBJECT_OT_create_collections)
    bpy.utils.register_class(VIEW3D_PT_collection_template)
    # Trigger the collection creation on startup and when a new scene is created
    bpy.app.handlers.load_post.append(on_scene_update)
    bpy.app.handlers.depsgraph_update_post.append(on_scene_update)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_create_collections)
    bpy.utils.unregister_class(VIEW3D_PT_collection_template)
    bpy.app.handlers.load_post.remove(on_scene_update)
    bpy.app.handlers.depsgraph_update_post.remove(on_scene_update)

if __name__ == "__main__":
    register()