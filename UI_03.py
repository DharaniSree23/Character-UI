import pymel.core as pm

#### SAVE THE FILE
def save_file_as(*args):
    
    # Prompt the user to choose a new file path
    file_path = pm.fileDialog2(fileFilter='Maya ASCII (*.ma);;Maya Binary (*.mb)', dialogStyle=2, fileMode=0)

    # If the user canceled the dialog, file_path will be an empty list, so we check for that.
    if file_path:
        # Save the current Maya scene to the chosen file path using "Save As".
        pm.saveAs(file_path[0], type='mayaAscii')  # Use 'mayaBinary' for Maya Binary format (*.mb).

#### IMPORT MODEL
def import_model_into_scene(*args):
    file_path = pm.fileDialog2(fileMode=1, caption="Rig Build", fileFilter="Maya Files (*.ma *.mb);;All Files (*.*)")
  
    if not file_path:
        pm.warning("No file selected.")
        return
       
    pm.importFile(file_path[0], returnNewNodes=True)
    top_group = pm.ls('*', assemblies=True)[0]
    top_group.rename('Model_Grp')
   
    parent_group = pm.group(empty=True, name="Ava")
    pm.parent(top_group, parent_group)


#### IMPORT JOINTS AND CONTROLS            
def import_joints_and_ctrls_and_constrain():
    fileJoints_path ='D:/Job/Personal projects/GUI_Rig build/Joints/Ava_Jnts.ma'
    pm.importFile(fileJoints_path,returnNewNodes=True)
    
    fileControls_path ='D:/Job/Personal projects/GUI_Rig build/Controls/Ctrls.ma'
    pm.importFile(fileControls_path,returnNewNodes=True)

    imported_joints = pm.ls('*_Jnts', type='joint')
    imported_ctrls = pm.ls('*_Ctrl')


    if not imported_joints or not imported_ctrls:
        pm.warning("No joints or controls found in the imported file.")
        return  
    
    for ctrl in imported_ctrls:
        ctrl_name = ctrl.stripNamespace().split(':')[-1]
        joint_name = ctrl_name.replace('_Ctrl', '_Jnts')

        if pm.objExists(joint_name):
            joint = pm.PyNode(joint_name)

            pm.parentConstraint(ctrl, joint, maintainOffset=True)
         
####  SKIN THE MESH    
def skin_mesh_to_skeleton(mesh_name, root_joint):
    if not pm.objExists(mesh_name):
        print("Mesh '{}' not found.".format(mesh_name))
        return None

    if not pm.objExists(root_joint):
        print("Root joint '{}' not found.".format(root_joint))
        return None
        
    root_joint = pm.PyNode(root_joint)
   
    skeleton_joints = root_joint.getChildren(allDescendents=True, type='joint')
        
    skin_cluster = pm.skinCluster(skeleton_joints, mesh_name, toSelectedBones=True, bindMethod=0)
    pm.skinPercent(skin_cluster, mesh_name, normalize=True)
  
    joints_group = pm.PyNode(joints_group_name)
    controls_group = pm.PyNode(controls_group_name)
    characterName_group = pm.PyNode(characterName_group_name)

    # Parent the child group under the parent group
    pm.parent(joints_group, characterName_group)
    pm.parent(controls_group, characterName_group)
    return skeleton_joints

joints_group_name = 'Joints_Grp'
controls_group_name = 'Controls_Grp'
characterName_group_name = 'Ava'
    
    
mesh_name = 'Body'
root_joint = 'Hips_Jnts' 
  
#### LOAD WEIGHTS

def load_skin_weights(mesh_name, weights_file_path):
    # Check if the specified mesh exists
    if not pm.objExists(mesh_name):
        print("Mesh '{}' not found.".format(mesh_name))
        return

    # Check if the weights file exists
    if not pm.system.doesFileExist(weights_file_path):
        print("Weights file '{}' not found.".format(weights_file_path))
        return

    # Load skin weights from the file onto the specified mesh
    pm.deformerWeights(mesh_name, im=weights_file_path)

mesh_name = 'Body'
weights_file_path = 'D:\Job\Personal projects\GUI_Rig build\Skin\Body_Skin.xml'


#### FUNCTIONS TO CALL IN UI

def save_file(*args):
    save_file_as()

def import_model(*args):
    import_model_into_scene()
       
def import_Jnts_Ctrls(*args):
    import_joints_and_ctrls_and_constrain()

def import_skin(*args):
    skin_mesh_to_skeleton(mesh_name, root_joint)
    
def import_weights(*args):
    load_skin_weights(mesh_name, weights_file_path)
 
def create_ui():
    if pm.window("importModelWindow", exists=True):
        pm.deleteUI("importModelWindow", window=True)

    window = pm.window("importModelWindow", title="Rig Build", widthHeight=(300, 100))
    main_layout = pm.columnLayout(adjustableColumn=True)
    
    pm.layout(main_layout, edit=True, backgroundColor=[0.4, 0.4, 0.4])
    #pm.text(label="This is a custom UI window.", backgroundColor=[0.18, 0.24, 0.31])

    pm.text(label="click the button below to import:")
    pm.separator(style="none", height=5)

    #pm.button(label="Model",bgc=[0.467, 0.765, 0.961], command=import_model)
    pm.button(label="Save the scene",bgc=[0.78,0.89,0.89], command=save_file)
    pm.separator(height=2)
    pm.button(label="Model",bgc=[0.78,0.89,0.89], command=import_model)
    pm.separator(height=2)
    pm.button(label="Joints/Controls",bgc=[0.78,0.89,0.89], command=import_Jnts_Ctrls)
    pm.separator(height=2)
    pm.button(label="Skin",bgc=[0.78,0.89,0.89], command=import_skin)
    pm.separator(height=2)
    pm.button(label="Load Weights (WIP)",bgc=[0.78,0.89,0.89], command=import_weights)
    pm.separator(height=2)
    pm.button(label="Surfacing (WIP)",bgc=[0.78,0.89,0.89], command=import_model)
    pm.separator(height=2)
    pm.button(label="Anim Test (WIP)",bgc=[0.78,0.89,0.89], command=import_model)
   

    window.show()

create_ui()

