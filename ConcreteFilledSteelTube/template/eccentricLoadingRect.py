# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2022 replay file
# Internal Version: 2021_09_16-01.57.30 176069
# Run by Administrator on Fri Oct 21 22:16:36 2022

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
from mesh import *


session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=303.544281005859, 
    height=148.296295166016)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()

from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
from material import *
# from .pyScript.modelMaterials.materials import *


section_height = 108.0
section_width = 108.0
thickness = 4.0
steel_yield = 400.0
fc = 120.0
ft = 7.0

height = section_height*3
plate_rectangle_size = max(section_height,section_width)+50
plate_thickness = 35.0
concrete_meshsize = 9
steel_meshsize = 9
plate_meshsize = 9

load_displacement_target = height/10

e = 10

model_name = 'bending_analysis'

# model create 

mdb.Model(model_name)

if "Model-1" in mdb.models:
    del mdb.models['Model-1']


# tube part
current_model = mdb.models[model_name]
s_steel_tube = current_model.ConstrainedSketch(name='tube', 
    sheetSize=200.0)
s_steel_tube.rectangle(point1=(-section_width/2,-section_height/2), point2=(section_width/2, section_height/2))
s_steel_tube.rectangle(point1=(-section_width/2+thickness, -section_height/2+thickness), point2=(section_width/2-thickness, section_height/2-thickness))
part_tube = current_model.Part(name='tube', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
part_tube.BaseSolidExtrude(sketch=s_steel_tube, depth=height)

# concrete part
s_concrete = current_model.ConstrainedSketch(name='concrete', 
    sheetSize=200.0)
s_concrete.rectangle(point1=(-section_width/2+thickness, -section_height/2+thickness), point2=(section_width/2-thickness, section_height/2-thickness))

part_concrete = current_model.Part(name='concrete', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
part_concrete.BaseSolidExtrude(sketch=s_concrete, depth=height)

# plate part
s_plate = current_model.ConstrainedSketch(name='plate', 
    sheetSize=200.0)
s_plate.rectangle(point1=(-plate_rectangle_size/2,-plate_rectangle_size/2),point2=(plate_rectangle_size/2,plate_rectangle_size/2))

part_plate = current_model.Part(name='plate', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
part_plate.BaseSolidExtrude(sketch=s_plate, depth=plate_thickness)


# Assembly
assembly = current_model.rootAssembly
instance_concrete = assembly.Instance("instance_concrete",part_concrete,dependent=True)
instance_tube = assembly.Instance("instance_tube",part_tube,dependent=True)
instance_plate1 = assembly.Instance("instance_plate1",part_plate,dependent=True)
instance_plate2 = assembly.Instance("instance_plate2",part_plate,dependent=True)

# plate1 at the bottom and plate2 at the top 
assembly.translate(('instance_plate1',),(0,0,-plate_thickness))
assembly.translate(('instance_plate2',),(0,0,height))

# surface 
assembly.Surface(side12Faces=instance_plate1.faces.findAt(((0,0,0),)),name='plate1_tie')

assembly.Surface(side12Faces=instance_plate2.faces.findAt(((0,0,height),)),name='plate2_tie')

assembly.Set(faces=instance_plate1.faces.findAt(((0,0,0-plate_thickness),)),name='plate1_fix')
assembly.Set(faces=instance_plate2.faces.findAt(((0,0,height+plate_thickness),)),name='plate2_load')


assembly.Surface(side12Faces=instance_tube.faces.findAt(((section_width/2-thickness/2,section_height/2-thickness/2,0),)),name='tube1_tie')
assembly.Surface(side12Faces=instance_tube.faces.findAt(((section_width/2-thickness/2,section_height/2-thickness/2,height),)),name='tube2_tie')

tube_contact_surface_find_at_points_x_abs = section_width/2-thickness
tube_contact_surface_find_at_points_y_abs = section_height/2-thickness

tube_contact_surface_find_at_points = (
    ((tube_contact_surface_find_at_points_x_abs,0,height/2),),
    ((-tube_contact_surface_find_at_points_x_abs,0,height/2),),
    ((0,tube_contact_surface_find_at_points_y_abs,height/2),),
    ((0,-tube_contact_surface_find_at_points_y_abs,height/2),),
    )
assembly.Surface(side12Faces=instance_tube.faces.findAt(*tube_contact_surface_find_at_points),name='tube_contact')

# constrain
current_model.Tie(name='plate_tie-1', main=assembly.surfaces['plate1_tie'], secondary=assembly.surfaces['tube1_tie'], 
    positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
current_model.Tie(name='plate_tie-2', main=assembly.surfaces['plate2_tie'], secondary=assembly.surfaces['tube2_tie'], 
    positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)



# fix and load edge get 
dp1 = part_plate.DatumPointByCoordinate(coords=(1,e,0))
dp2 = part_plate.DatumPointByCoordinate(coords=(0,e,0))
dp3 = part_plate.DatumPointByCoordinate(coords=(0,e,plate_thickness))
dp_1 = part_plate.datums[dp1.id]
dp_2 = part_plate.datums[dp2.id]
dp_3 = part_plate.datums[dp3.id]
cells_to_be_partititon = part_plate.cells.findAt(((0,e,0),))
part_plate.PartitionCellByPlaneThreePoints(point1=dp_1,point2=dp_2,point3=dp_3,cells=cells_to_be_partititon)


fix_plate_edge = assembly.instances['instance_plate1'].edges
fix_edge = fix_plate_edge.findAt(((0,e,-plate_thickness),))
assembly.Set(edges=fix_edge, name='fix_edge')

load_plate_edge = assembly.instances['instance_plate2'].edges
load_edge = load_plate_edge.findAt(((0,e,plate_thickness+height),))
assembly.Set(edges=load_edge, name='load_edge')


for i in range(1,int(height/concrete_meshsize)):
    # datum setting 
    dp_1_feature = part_concrete.DatumPointByCoordinate((section_width/2-thickness,0,concrete_meshsize*i))
    dp_2_feature = part_concrete.DatumPointByCoordinate((0,section_height/2-thickness,concrete_meshsize*i))
    dp_3_feature = part_concrete.DatumPointByCoordinate((-section_width/2+thickness,0,concrete_meshsize*i))
    
    dp_1 = part_concrete.datums[dp_1_feature.id]
    dp_2 = part_concrete.datums[dp_2_feature.id]
    dp_3 = part_concrete.datums[dp_3_feature.id]
    # partition concrete
    cells_to_be_partititon = part_concrete.cells.findAt(((0,0,concrete_meshsize*(i+0.5)),))
    part_concrete.PartitionCellByPlaneThreePoints(point1=dp_1,point2=dp_2,point3=dp_3,cells=cells_to_be_partititon)



    
cohesive_faces_findat_value = []
contact_faces_findat_value = []
for i in range(1,int(height/concrete_meshsize)): 
    cohesive_faces_findat_value.append(((0,0,concrete_meshsize*i),))
    contact_faces_findat_value.append(((section_width/2-thickness,0,concrete_meshsize*(i+0.5)),))
    contact_faces_findat_value.append(((-section_width/2+thickness,0,concrete_meshsize*(i+0.5)),))
    contact_faces_findat_value.append(((0,section_height/2-thickness,concrete_meshsize*(i+0.5)),))
    contact_faces_findat_value.append(((0,-section_height/2+thickness,concrete_meshsize*(i+0.5)),))
    
   
contact_faces_findat_value.append(((section_width/2-thickness,0,concrete_meshsize*0.5),))

cohesive_faces = part_concrete.faces.findAt(*(tuple(cohesive_faces_findat_value)))
part_concrete.Surface(side1Faces=cohesive_faces,name='cohesive_face')

contact_faces = part_concrete.faces.findAt(*contact_faces_findat_value)
part_concrete.Surface(side1Faces=contact_faces,name='contact_face')

plate1_contact_faces = part_concrete.faces.findAt(((0,0,0),))
part_concrete.Surface(side1Faces=plate1_contact_faces,name='plate1_contact_faces')

plate2_contact_faces = part_concrete.faces.findAt(((0,0,height),))
part_concrete.Surface(side1Faces=plate2_contact_faces,name='plate2_contact_faces')


## concrete partition to better mesh 
dp_1_feature = part_concrete.DatumPointByCoordinate((section_width/2-thickness,0,0))
dp_2_feature = part_concrete.DatumPointByCoordinate((-section_width/2+thickness,0,0))
dp_3_feature = part_concrete.DatumPointByCoordinate((section_width/2-thickness,0,height))

dp_1 = part_concrete.datums[dp_1_feature.id]
dp_2 = part_concrete.datums[dp_2_feature.id]
dp_3 = part_concrete.datums[dp_3_feature.id]
cells_to_be_partititon = part_concrete.cells
part_concrete.PartitionCellByPlaneThreePoints(point1=dp_1,point2=dp_2,point3=dp_3,cells=cells_to_be_partititon)

dp_1_feature = part_concrete.DatumPointByCoordinate((0,section_height/2-thickness,0))
dp_2_feature = part_concrete.DatumPointByCoordinate((0,-section_height/2+thickness,0))
dp_3_feature = part_concrete.DatumPointByCoordinate((0,section_height/2-thickness,height))

dp_1 = part_concrete.datums[dp_1_feature.id]
dp_2 = part_concrete.datums[dp_2_feature.id]
dp_3 = part_concrete.datums[dp_3_feature.id]
cells_to_be_partititon = part_concrete.cells
part_concrete.PartitionCellByPlaneThreePoints(point1=dp_1,point2=dp_2,point3=dp_3,cells=cells_to_be_partititon)


## steel partition to better mesh 
dp_1_feature = part_tube.DatumPointByCoordinate((section_width/2-thickness,0,0))
dp_2_feature = part_tube.DatumPointByCoordinate((-section_width/2+thickness,0,0))
dp_3_feature = part_tube.DatumPointByCoordinate((section_width/2-thickness,0,height))

dp_1 = part_tube.datums[dp_1_feature.id]
dp_2 = part_tube.datums[dp_2_feature.id]
dp_3 = part_tube.datums[dp_3_feature.id]
cells_to_be_partititon = part_tube.cells
part_tube.PartitionCellByPlaneThreePoints(point1=dp_1,point2=dp_2,point3=dp_3,cells=cells_to_be_partititon)

dp_1_feature = part_tube.DatumPointByCoordinate((0,section_height/2-thickness,0))
dp_2_feature = part_tube.DatumPointByCoordinate((0,-section_height/2+thickness,0))
dp_3_feature = part_tube.DatumPointByCoordinate((0,section_height/2-thickness,height))

dp_1 = part_tube.datums[dp_1_feature.id]
dp_2 = part_tube.datums[dp_2_feature.id]
dp_3 = part_tube.datums[dp_3_feature.id]
cells_to_be_partititon = part_tube.cells
part_tube.PartitionCellByPlaneThreePoints(point1=dp_1,point2=dp_2,point3=dp_3,cells=cells_to_be_partititon)


## create step 
current_model.StaticStep(name='Step-1', previous='Initial', 
    timePeriod=1.0, maxNumInc=2000,initialInc=0.005,minInc=1E-8,maxInc=0.05)
assembly.Set(faces=instance_plate1.faces.findAt(((0,0,0-plate_thickness),)),name='plate1_fix')
assembly.Set(faces=instance_plate2.faces.findAt(((0,0,height+plate_thickness),)),name='plate2_load')

# fix add 
region = assembly.sets["fix_edge"]
mdb.models[model_name].DisplacementBC(name='Pinned : ', 
createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET, 
ur2=UNSET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, 
fieldName='', localCsys=None)


# load add 
region = assembly.sets['load_edge']
mdb.models[model_name].DisplacementBC(name='displacement', 
    createStepName='Step-1', region=region, u1=0.0, u2=0.0, u3 = load_displacement_target, 
    ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)


# mesh 
part_concrete.seedPart(size=concrete_meshsize,deviationFactor=0.1, minSizeFactor=0.1)
part_concrete.generateMesh()
part_tube.seedPart(size=steel_meshsize,deviationFactor=0.1, minSizeFactor=0.1)
part_tube.generateMesh()
part_plate.seedPart(size=plate_meshsize,deviationFactor=0.1, minSizeFactor=0.1)
part_plate.generateMesh()

part_concrete.Set(elements=part_concrete.elements,name='concrete_base')


## insert cohesize
# side1Faces = part_concrete.surfaces['cohesive_face']
# part_concrete.insertElements(faces=side1Faces)
# # #: Inserted 612 cohesive pore pressure elements by addition of 1564 new nodes, of which 782 are midside nodes
# concrete_ele = part_concrete.elements
# concrete_base_ele = part_concrete.sets['concrete_base'].elements
# concrete_cohesive_ele = concrete_ele[len(concrete_base_ele):]

# part_concrete.Set(elements=concrete_cohesive_ele,name='concrete_cohesive')


# elemType1 = mesh.ElemType(elemCode=COH3D8, elemLibrary=STANDARD)
# part_concrete.setElementType(regions=part_concrete.sets['concrete_cohesive'], elemTypes=(elemType1, ))


## contact
current_model.ContactProperty('steel_concrete')
current_model.interactionProperties['steel_concrete'].TangentialBehavior(
    formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
    pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
    0.3, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
    fraction=0.1, elasticSlipStiffness=None)
current_model.interactionProperties['steel_concrete'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=OFF, 
    constraintEnforcementMethod=DEFAULT)

current_model.SurfaceToSurfaceContactStd(name='steel_concrete', 
    createStepName='Step-1', 
    main=assembly.instances['instance_concrete'].surfaces['contact_face'], 
    secondary=assembly.surfaces['tube_contact'], 
    sliding=FINITE, 
    thickness=ON, interactionProperty='steel_concrete', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

current_model.SurfaceToSurfaceContactStd(name='plate1_concrete', 
    createStepName='Step-1', 
    main=assembly.instances['instance_concrete'].surfaces['plate1_contact_faces'], 
    secondary=assembly.surfaces['plate1_tie'], 
    sliding=FINITE, 
    thickness=ON, interactionProperty='steel_concrete', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

current_model.SurfaceToSurfaceContactStd(name='plate2_concrete', 
    createStepName='Step-1', 
    main=assembly.instances['instance_concrete'].surfaces['plate2_contact_faces'], 
    secondary=assembly.surfaces['plate2_tie'], 
    sliding=FINITE, 
    thickness=ON, interactionProperty='steel_concrete', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
#: The interaction "Int-1" has been created.

## load
 
# current_model.EncastreBC(name='fix', createStepName='Initial', 
# #    region=assembly.sets['plate1_fix'], localCsys=None)

# current_model.TabularAmplitude(name='disp_amp', timeSpan=STEP, 
#     smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (1.0, height/10)))

# current_model.DisplacementBC(name='load', createStepName='Step-1', 
# #    region=assembly.sets['plate2_load'], u1=UNSET, u2=UNSET, u3=1.0, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
#     amplitude='disp_amp', fixed=OFF, distributionType=UNIFORM, fieldName='', 
#     localCsys=None)

# #: The interaction property "IntProp-1" has been created.


## material
### steel

## material
### steel
from materials import steelBialinear,plateRigid,abaqus_concrete_params
tube_steel_para_dict = steelBialinear(steel_yield)
current_model.Material(name='tube_steel')
current_model.materials['tube_steel'].Density(table=tube_steel_para_dict['Density'])
current_model.materials['tube_steel'].Elastic(table=(tube_steel_para_dict['Elastic'],))
current_model.materials['tube_steel'].Plastic(
    scaleStress=None, table=tube_steel_para_dict['Plastic'])

current_model.HomogeneousSolidSection(name='tube_steel', 
    material='tube_steel', thickness=None)


plate_steel_para_dict = plateRigid()
current_model.Material(name='plate_rigid')
current_model.materials['plate_rigid'].Density(table=plate_steel_para_dict['Density'])
current_model.materials['plate_rigid'].Elastic(table=(plate_steel_para_dict['Elastic'],))
current_model.materials['plate_rigid'].Plastic(
    scaleStress=None, table=plate_steel_para_dict['Plastic'])

current_model.HomogeneousSolidSection(name='plate_rigid', 
    material='plate_rigid', thickness=None)


concrete_para_dict = abaqus_concrete_params(fc,ft)
current_model.Material(name='concrete')
current_model.materials['concrete'].Density(table=concrete_para_dict['Density'])
current_model.materials['concrete'].Elastic(table=concrete_para_dict['Elastic'])
current_model.materials['concrete'].ConcreteDamagedPlasticity(table=concrete_para_dict['CDP'])
current_model.materials['concrete'].concreteDamagedPlasticity.ConcreteCompressionHardening(
    table=concrete_para_dict['CompressionHardening'])
current_model.materials['concrete'].concreteDamagedPlasticity.ConcreteTensionStiffening(
    table=concrete_para_dict['TensionStiffening'])
current_model.materials['concrete'].concreteDamagedPlasticity.ConcreteCompressionDamage(
    table=concrete_para_dict['CompressionDamage'])
current_model.materials['concrete'].concreteDamagedPlasticity.ConcreteTensionDamage(
    table=concrete_para_dict['TensionDamage'])


current_model.HomogeneousSolidSection(name='concrete', material='concrete', thickness=None)


# cohesive_para_dict = cohesive()
# current_model.Material(name='cohesive')
# current_model.materials['cohesive'].Density(table=cohesive_para_dict['Density'])
# current_model.materials['cohesive'].QuadsDamageInitiation(table=cohesive_para_dict['QuadsDamage'])
# current_model.materials['cohesive'].quadsDamageInitiation.DamageEvolution(
#     type=ENERGY, mixedModeBehavior=BK, power=1.2, table=cohesive_para_dict['DamageEvolution'])
# current_model.materials['cohesive'].Elastic(type=TRACTION, table=cohesive_para_dict['ElasticTraction'])

# current_model.CohesiveSection(name='cohesive', material='cohesive', 
#     response=TRACTION_SEPARATION, outOfPlaneThickness=None)


part_plate.SectionAssignment(region=(part_plate.cells,), sectionName='plate_rigid', 
    offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)


part_tube.SectionAssignment(region=(part_tube.cells,), sectionName='tube_steel', 
    offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

part_concrete.SectionAssignment(region=part_concrete.sets['concrete_base'],sectionName='concrete',
    offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)

# part_concrete.SectionAssignment(region=part_concrete.sets['concrete_cohesive'],sectionName='cohesive',
#     offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', 
#     thicknessAssignment=FROM_SECTION)


# ## output
current_model.FieldOutputRequest(name='damage_concrete', createStepName='Step-1', 
    variables=('DAMAGEC', 'DAMAGET'))

current_model.FieldOutputRequest(name='displacement', 
    createStepName='Step-1', variables=('UT', ), region=assembly.sets['load_edge'], 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

current_model.FieldOutputRequest(name='force', createStepName='Step-1', 
    variables=('RF', ), region=assembly.sets['load_edge'], 
    sectionPoints=DEFAULT, rebar=EXCLUDE)



mdb.Job(name=model_name, model=model_name, description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, explicitPrecision=DOUBLE_PLUS_PACK, 
    nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
    contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
    resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=20, 
    activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=20)

mdb.jobs[model_name].submit(consistencyChecking=OFF)