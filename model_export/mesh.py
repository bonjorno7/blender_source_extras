import bpy
import bmesh
import mathutils
from .. import common


class MeshProps(bpy.types.PropertyGroup):
    """Properties for a mesh"""
    bl_idname = "BASE_PG_MeshProps"

    obj: bpy.props.PointerProperty(
        name="Mesh Object",
        description="Object that holds the data for this mesh",
        type=bpy.types.Object,
        poll=common.is_mesh,
    )

    kind: bpy.props.EnumProperty(
        name="Mesh Type",
        description="Whether this mesh should be Reference (visible) or Collision (tangible)",
        items=(
            ('REFERENCE', "REF", "Reference"),
            ('COLLISION', "COL", "Collision"),
        ),
    )


class MeshList(bpy.types.UIList):
    """List of meshes for this model"""
    bl_idname = "BASE_UL_MeshList"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row().split(factor=0.6)
        row.label(text=item.obj.name)
        row.split().row().prop(item, "kind", expand=True)


class AddMesh(bpy.types.Operator):
    """Add selected objects as meshes to this model"""
    bl_idname = "base.add_mesh"
    bl_label = "Add Mesh"

    def execute(self, context):
        base = context.scene.BASE
        model = base.models[base.model_index]

        for o in context.selected_objects:
            if o.type == 'MESH':
                duplicate = False

                for m in model.meshes:
                    if m.obj == o:
                        duplicate = True

                if not duplicate:
                    model.meshes.add()
                    mesh = model.meshes[-1]
                    mesh.obj = o

                    if mesh.obj.name.find(".col") != -1:
                        mesh.kind = 'COLLISION'

        model.mesh_index = len(model.meshes) - 1
        return {'FINISHED'}


class RemoveMesh(bpy.types.Operator):
    """Remove selected mesh from the list"""
    bl_idname = "base.remove_mesh"
    bl_label = "Remove Mesh"

    @classmethod
    def poll(cls, context):
        base = context.scene.BASE
        if len(base.models) > 0:
            model = base.models[base.model_index]
            return len(model.meshes) > 0
        return False

    def execute(self, context):
        base = context.scene.BASE
        model = base.models[base.model_index]
        model.meshes.remove(model.mesh_index)
        model.mesh_index = min(
            max(0, model.mesh_index - 1), len(model.meshes) - 1)
        return {'FINISHED'}


class MoveMesh(bpy.types.Operator):
    """Move the selected mesh up or down in the list"""
    bl_idname = "base.move_mesh"
    bl_label = "Move Mesh"

    direction: bpy.props.EnumProperty(items=(
        ('UP', "Up", "Move the item up"),
        ('DOWN', "Down", "Move the item down"),
    ))

    @classmethod
    def poll(cls, context):
        base = context.scene.BASE
        model = base.models[base.model_index]
        return len(model.meshes) > 1

    def execute(self, context):
        base = context.scene.BASE
        model = base.models[base.model_index]
        neighbor = model.mesh_index + (-1 if self.direction == 'UP' else 1)
        model.meshes.move(neighbor, model.mesh_index)
        list_length = len(model.meshes) - 1
        model.mesh_index = max(0, min(neighbor, list_length))
        return {'FINISHED'}
