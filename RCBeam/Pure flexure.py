# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.13-1 replay file
# Internal Version: 2013_05_16-10.28.56 126354
# Run by Ray on Sat Nov 21 19:26:18 2020
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *


###creat current Viewport
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=289.849975585938, 
    height=196.785186767578)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
Mdb()
#: A new model database has been created.
#: The model "Model-1" has been created.


###Material defination
##Concrete canbe prarlized
mdb.models['Model-1'].Material(name='Concrete C25')
mdb.models['Model-1'].materials['Concrete C25'].Density(table=((2400.0, ), ))
mdb.models['Model-1'].materials['Concrete C25'].Elastic(table=((15400000000.0, 
    0.2), ))
mdb.models['Model-1'].materials['Concrete C25'].ConcreteDamagedPlasticity(
    table=((40.0, 0.1, 1.225, 0.6667, 0.0005), ))
mdb.models['Model-1'].materials['Concrete C25'].concreteDamagedPlasticity.ConcreteCompressionHardening(
    table=((5020000.0, 0.0), (9230000.0, 6.025e-05), (12500000.0, 0.0001815), (
    14800000.0, 0.0003637), (16300000.0, 0.0006069), (16700000.0, 0.0009111), (
    14200000.0, 0.002874), (836.0, 0.02)))
mdb.models['Model-1'].materials['Concrete C25'].concreteDamagedPlasticity.ConcreteTensionStiffening(
    table=((1670000.0, 0.0), ))

##Steel     ###canbeparalized
mdb.models['Model-1'].Material(name='Constrain steel HPB300')
mdb.models['Model-1'].materials['Constrain steel HPB300'].Density(table=((
    7850.0, ), ))
mdb.models['Model-1'].materials['Constrain steel HPB300'].Elastic(table=((
    210000000000.0, 0.3), ))
mdb.models['Model-1'].materials['Constrain steel HPB300'].Plastic(table=((
    270000000.0, 0.0), (816000000.0, 0.2574)))
mdb.models['Model-1'].Material(name='Longitude Steel HRB400')
mdb.models['Model-1'].materials['Longitude Steel HRB400'].Density(table=((
    7850.0, ), ))
mdb.models['Model-1'].materials['Longitude Steel HRB400'].Elastic(table=((
    210000000000.0, 0.3), ))
mdb.models['Model-1'].materials['Longitude Steel HRB400'].Plastic(table=((
    360000000.0, 0.0), (906000000.0, 0.2574)))



### Concrete Part
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-0.1, -0.2), point2=(0.1, 0.2))                        ###########canBeParalized

p = mdb.models['Model-1'].Part(name='Concrete', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=3.0)                    ###########canBeParalized Beam 
s.unsetPrimaryObject()
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

##create reference get Pure Flxure edge 
v = p.vertices
p.DatumPointByOffset(point=v[3], vector=(0.0, 0.0, 0.05))
p.DatumPointByOffset(point=v[0], vector=(0.0, 0.0, -0.05))
p.DatumPointByOffset(point=v[2], vector=(0.0, 0.0, 1.0))
v, d = p.vertices, p.datums
p.DatumPointByOffset(point=d[4], vector=(0.0, 0.0, 0.025))

v, d2 = p.vertices, p.datums
p.DatumPointByOffset(point=d2[4], vector=(0.0, 0.0, -0.025))

p = mdb.models['Model-1'].parts['Concrete']
v2, d1 = p.vertices, p.datums
p.DatumPointByOffset(point=v2[1], vector=(0.0, 0.0, -1.0))
p = mdb.models['Model-1'].parts['Concrete']
v1, d2 = p.vertices, p.datums
p.DatumPointByOffset(point=d2[7], vector=(0.0, 0.0, 0.025))
p = mdb.models['Model-1'].parts['Concrete']
v2, d1 = p.vertices, p.datums
p.DatumPointByOffset(point=d1[7], vector=(0.0, 0.0, -0.025))

p = mdb.models['Model-1'].parts['Concrete']
v1, d2 = p.vertices, p.datums
p.DatumPointByMidPoint(point1=v1[3], point2=d2[2])
p = mdb.models['Model-1'].parts['Concrete']
v2, d1 = p.vertices, p.datums
p.DatumPointByMidPoint(point1=d1[3], point2=v2[0])


p = mdb.models['Model-1'].parts['Concrete']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
e, v1, d2 = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(point=d2[2], normal=e[3], cells=pickedCells)
p = mdb.models['Model-1'].parts['Concrete']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
e1, v2, d1 = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(point=d1[6], normal=e1[10], 
    cells=pickedCells)
p = mdb.models['Model-1'].parts['Concrete']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
e, v1, d2 = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(point=d2[5], normal=e[6], cells=pickedCells)
session.viewports['Viewport: 1'].view.setValues(nearPlane=5.7448, 
    farPlane=6.3878, width=2.36805, height=1.16051, viewOffsetX=-0.193833, 
    viewOffsetY=-0.0214807)
p = mdb.models['Model-1'].parts['Concrete']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#4 ]', ), )
e1, v2, d1 = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(point=d1[9], normal=e1[4], cells=pickedCells)
p = mdb.models['Model-1'].parts['Concrete']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
e, v1, d2 = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(point=d2[8], normal=e[16], cells=pickedCells)
session.viewports['Viewport: 1'].view.setValues(nearPlane=5.72848, 
    farPlane=6.40412, width=2.54301, height=1.24625, viewOffsetX=0.205856, 
    viewOffsetY=-0.0677503)
p = mdb.models['Model-1'].parts['Concrete']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
e1, v2, d1 = p.edges, p.vertices, p.datums
p.PartitionCellByPlanePointNormal(point=d1[3], normal=e1[10], 
    cells=pickedCells)
session.viewports['Viewport: 1'].view.setValues(nearPlane=4.78739, 
    farPlane=7.07313, width=2.12524, height=1.04151, cameraPosition=(-4.66337, 
    1.96565, -1.59179), cameraUpVector=(0.359009, 0.932184, 0.0463128), 
    cameraTarget=(0.133826, -0.0372181, 1.53478), viewOffsetX=0.172038, 
    viewOffsetY=-0.0566201)
session.viewports['Viewport: 1'].view.setValues(nearPlane=4.82474, 
    farPlane=7.03577, width=2.14182, height=1.04964, cameraPosition=(-4.66416, 
    1.96178, -1.59305), cameraUpVector=(0.368101, 0.929285, 0.0305055), 
    cameraTarget=(0.133033, -0.041084, 1.53352), viewOffsetX=0.17338, 
    viewOffsetY=-0.0570619)
session.viewports['Viewport: 1'].view.setValues(nearPlane=4.82328, 
    farPlane=7.03723, width=2.14117, height=1.04932, cameraPosition=(-4.66118, 
    1.9776, -1.58748), cameraUpVector=(0.329931, 0.939172, 0.0954047), 
    cameraTarget=(0.136008, -0.025261, 1.53909), viewOffsetX=0.173328, 
    viewOffsetY=-0.0570446)
session.viewports['Viewport: 1'].view.setValues(nearPlane=4.70761, 
    farPlane=7.15289, width=3.66211, height=1.79469, viewOffsetX=0.450717, 
    viewOffsetY=0.00566753)
session.viewports['Viewport: 1'].view.setValues(nearPlane=4.69054, 
    farPlane=7.16996, width=3.64883, height=1.78818, cameraPosition=(-4.69001, 
    1.90538, -1.58951), cameraUpVector=(0.397297, 0.917429, -0.0218852), 
    cameraTarget=(0.107178, -0.0974817, 1.53706), viewOffsetX=0.449084, 
    viewOffsetY=0.00564699)
session.viewports['Viewport: 1'].view.setValues(nearPlane=4.86316, 
    farPlane=6.99734, width=1.59089, height=0.779645, viewOffsetX=-0.458548, 
    viewOffsetY=0.132861)
session.viewports['Viewport: 1'].view.setValues(session.views['Left'])
p = mdb.models['Model-1'].parts['Concrete']
v1 = p.vertices
p.DatumPointByOffset(point=v1[30], vector=(0.0, -0.041, 0.0))
p = mdb.models['Model-1'].parts['Concrete']
v2 = p.vertices
p.DatumPointByOffset(point=v2[28], vector=(0.0, 0.041, 0.0))
p = mdb.models['Model-1'].parts['Concrete']
v1 = p.vertices
p.DatumPointByOffset(point=v1[5], vector=(0.0, 0.0, 41.0))
p = mdb.models['Model-1'].parts['Concrete']
v2 = p.vertices
p.DatumPointByOffset(point=v2[5], vector=(0.0, 0.041, 0.0))
p = mdb.models['Model-1'].parts['Concrete']
v1 = p.vertices
p.DatumPointByOffset(point=v1[11], vector=(0.0, -0.041, 0.0))
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].materials.changeKey(fromName='Constrain steel HPB300', 
    toName='Constrain and above steel HPB300')
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.Line(point1=(0.0, 0.0), point2=(1.0, 0.0))
s1.HorizontalConstraint(entity=g[2], addUndoState=False)
session.viewports['Viewport: 1'].view.setValues(nearPlane=188.158, 
    farPlane=188.966, width=4.3107, height=2.18906, cameraPosition=(0.939745, 
    -0.0124419, 188.562), cameraTarget=(0.939745, -0.0124419, 0))
p = mdb.models['Model-1'].Part(name='Part-2', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-2']
p.BaseWire(sketch=s1)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-2']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].parts.changeKey(fromName='Part-2', toName='Down rebar')
mdb.models['Model-1'].parts.changeKey(fromName='Down rebar', toName='Up rebar')
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
#: Warning: Coincident point selected.
s.Line(point1=(0.0, 0.0), point2=(3.0, 0.0))
s.HorizontalConstraint(entity=g[2], addUndoState=False)
p = mdb.models['Model-1'].Part(name='Down rebar', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Down rebar']
p.BaseWire(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Down rebar']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.rectangle(point1=(-0.0865, -0.1865), point2=(0.0865, 0.1865))
session.viewports['Viewport: 1'].view.setValues(nearPlane=188.437, 
    farPlane=188.687, width=1.33038, height=0.675597, cameraPosition=(0.189273, 
    0.0134283, 188.562), cameraTarget=(0.189273, 0.0134283, 0))
p = mdb.models['Model-1'].Part(name='Constrain rebar', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Constrain rebar']
p.BaseWire(sketch=s1)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Constrain rebar']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.753342, 
    farPlane=0.891324, width=0.82857, height=0.406057, viewOffsetX=-0.015007, 
    viewOffsetY=0.00128453)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']
p1 = mdb.models['Model-1'].parts['Concrete']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.025, 0.0))
#: Number of geometries: 1
#: Number of vertices: 2
#: Number of constraints: 0 
#: Number of dimensions: 0
#: Number of unconstrained DOF:4 
session.viewports['Viewport: 1'].view.setValues(nearPlane=188.542, 
    farPlane=188.581, width=0.20788, height=0.105566, cameraPosition=(
    0.0174401, -0.00496948, 188.562), cameraTarget=(0.0174401, -0.00496948, 0))
s1.Line(point1=(0.0, -0.008), point2=(1.0, -0.008))
s1.HorizontalConstraint(entity=g[3], addUndoState=False)
session.viewports['Viewport: 1'].view.setValues(nearPlane=188.545, 
    farPlane=188.579, width=0.183683, height=0.0932781, cameraPosition=(
    0.0166383, -0.00623222, 188.562), cameraTarget=(0.0166383, -0.00623222, 0))
s1.Line(point1=(0.0, -0.008), point2=(-0.0515284761786461, -0.008))
s1.HorizontalConstraint(entity=g[4], addUndoState=False)
s1.ParallelConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
session.viewports['Viewport: 1'].view.setValues(width=0.172662, 
    height=0.0876814, cameraPosition=(0.0138806, -0.00635394, 188.562), 
    cameraTarget=(0.0138806, -0.00635394, 0))
s1.autoTrimCurve(curve1=g[4], point1=(-0.0322173908352852, 
    -0.00772311771288514))
s1.autoTrimCurve(curve1=g[3], point1=(0.0386014506220818, 
    -0.00761358672752976))
s1.autoTrimCurve(curve1=g[2], point1=(0.0110851433128119, 0.00881657935678959))
s1.autoTrimCurve(curve1=g[7], point1=(0.0159087162464857, 
    -0.00301313633099198))
s1.delete(objectList=(g[6], g[5]))
p = mdb.models['Model-1'].Part(name='up support', dimensionality=THREE_D, 
    type=ANALYTIC_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['up support']
p.AnalyticRigidSurfExtrude(sketch=s1, depth=0.2)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['up support']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.360535, 
    farPlane=0.541944, width=0.153816, height=0.0753807, 
    viewOffsetX=-0.00569844, viewOffsetY=-0.00445754)
p = mdb.models['Model-1'].parts['up support']
e = p.edges
p.DatumPointByMidPoint(point1=p.InterestingPoint(edge=e[3], rule=MIDDLE), 
    point2=p.InterestingPoint(edge=e[1], rule=MIDDLE))
p = mdb.models['Model-1'].parts['up support']
v2, e1, d2, n = p.vertices, p.edges, p.datums, p.nodes
p.ReferencePoint(point=d2[2])
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.359583, 
    farPlane=0.542896, width=0.184702, height=0.0905166, 
    viewOffsetX=0.000338204, viewOffsetY=-0.00558769)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.025, 0.0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=188.55, 
    farPlane=188.574, width=0.127236, height=0.0646129, cameraPosition=(
    0.00667659, 0.00106968, 188.562), cameraTarget=(0.00667659, 0.00106968, 0))
s.Line(point1=(9.26591455936432e-05, 0.00450013531371951), point2=(
    -0.0387646779417992, 0.00450013531371951))
s.HorizontalConstraint(entity=g[3], addUndoState=False)
s.Line(point1=(-0.0387646779417992, 0.00450013531371951), point2=(
    0.0434739291667938, 0.00450013531371951))
s.HorizontalConstraint(entity=g[4], addUndoState=False)
s.ParallelConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
s.autoTrimCurve(curve1=g[2], point1=(-0.0208305232226849, -0.0259299892932177))
s.autoTrimCurve(curve1=g[4], point1=(0.0381421521306038, -0.0109974350780249))
s.autoTrimCurve(curve1=g[5], point1=(0.0219852551817894, 
    -0.000585007015615702))
s.autoTrimCurve(curve1=g[7], point1=(0.0158456340432167, 0.00159433810040355))
s.delete(objectList=(g[3], g[6], g[6]))
s.Line(point1=(-0.0245916404934322, 0.00450013531371954), point2=(
    0.0245916404934322, 0.00450013531371951))
s.HorizontalConstraint(entity=g[9], addUndoState=False)
p = mdb.models['Model-1'].Part(name='Down support', dimensionality=THREE_D, 
    type=ANALYTIC_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['Down support']
p.AnalyticRigidSurfExtrude(sketch=s, depth=0.2)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Down support']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['Model-1'].parts['Concrete']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=87.0466, 
    farPlane=88.9625, width=9.15602, height=4.48709, viewOffsetX=-16.7865, 
    viewOffsetY=0.150705)
session.viewports['Viewport: 1'].view.setValues(nearPlane=87.0971, 
    farPlane=88.912, width=9.16133, height=4.48969, viewOffsetX=-18.9251, 
    viewOffsetY=0.0752868)
session.viewports['Viewport: 1'].view.setValues(nearPlane=87.494, 
    farPlane=88.5151, width=4.37994, height=2.14647, viewOffsetX=-19.9544, 
    viewOffsetY=-0.227359)
mdb.models['Model-1'].HomogeneousSolidSection(name='Concrete', 
    material='Concrete C25', thickness=None)
p = mdb.models['Model-1'].parts['Concrete']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#7f ]', ), )
region = p.Set(cells=cells, name='Set-1')
p = mdb.models['Model-1'].parts['Concrete']
p.SectionAssignment(region=region, sectionName='Concrete', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['Constrain rebar']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=0.749814, 
    farPlane=0.894852, width=0.87733, height=0.429952, viewOffsetX=0.00806868, 
    viewOffsetY=0.0155011)
mdb.models['Model-1'].TrussSection(name='Constrain steel', 
    material='Constrain and above steel HPB300', area=5.024e-05)
mdb.models['Model-1'].TrussSection(name='Down rebar', 
    material='Longitude Steel HRB400', area=0.000154)
mdb.models['Model-1'].TrussSection(name='Up rebar', 
    material='Constrain and above steel HPB300', area=0.000154)
p = mdb.models['Model-1'].parts['Constrain rebar']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#f ]', ), )
region = p.Set(edges=edges, name='Constrain bar')
p = mdb.models['Model-1'].parts['Constrain rebar']
p.SectionAssignment(region=region, sectionName='Constrain steel', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['Down rebar']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Down rebar']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(edges=edges, name='Set-1')
p = mdb.models['Model-1'].parts['Down rebar']
p.SectionAssignment(region=region, sectionName='Down rebar', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['Up rebar']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Up rebar']
e = p.edges
edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(edges=edges, name='Up bar')
p = mdb.models['Model-1'].parts['Up rebar']
p.SectionAssignment(region=region, sectionName='Up rebar', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
p = mdb.models['Model-1'].parts['up support']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Concrete']
a.Instance(name='Concrete-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].view.setValues(session.views['Bottom'])
session.viewports['Viewport: 1'].view.setValues(session.views['Right'])

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['up support']
a.Instance(name='up support-1', part=p, dependent=ON)

p1 = mdb.models['Model-1'].parts['Concrete']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
p = mdb.models['Model-1'].parts['Concrete']
del p.features['Datum pt-13']

p = mdb.models['Model-1'].parts['Constrain rebar']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Concrete']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Constrain rebar']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Down rebar']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Down support']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['Up rebar']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
p = mdb.models['Model-1'].parts['up support']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
a = mdb.models['Model-1'].rootAssembly
a.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)


a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('up support-1', ), axisPoint=(0.1, 0.0, 0.0), 
    axisDirection=(0.0, 0.2, 0.0), angle=90.0)
#: The instance up support-1 was rotated by 90. degrees about the axis defined by the point 100.E-03, 0., 0. and the vector 0., 200.E-03, 0.



a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('up support-1', ), vector=(-0.1, 0.225, 0.9))
#: The instance up support-1 was translated by -100.E-03, 225.E-03, 900.E-03 with respect to the assembly coordinate system

a = mdb.models['Model-1'].rootAssembly
a.LinearInstancePattern(instanceList=('up support-1', ), direction1=(1.0, 0.0, 
    0.0), direction2=(0.0, 1.0, 0.0), number1=1, number2=2, spacing1=0.2, 
    spacing2=0.017)

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('up support-1-lin-1-2', ), vector=(0.0, -0.017, 1.0))
#: The instance up support-1-lin-1-2 was translated by 0., -17.E-03, 1. with respect to the assembly coordinate system

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Down support']
a.Instance(name='Down support-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=6.03815, 
    farPlane=6.73564, width=1.09559, height=0.536917, viewOffsetX=-0.963298, 
    viewOffsetY=-0.147976)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('Down support-1', ), axisPoint=(-0.1, -0.2, 0.0), 
    axisDirection=(0.0, 0.4, 0.0), angle=90.0)
#: The instance Down support-1 was rotated by 90. degrees about the axis defined by the point -100.E-03, -200.E-03, 0. and the vector 0., 400.E-03, 0.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Down support-1', ), vector=(0.1, -0.225, 0.125))
#: The instance Down support-1 was translated by 100.E-03, -225.E-03, 125.E-03 with respect to the assembly coordinate system
a = mdb.models['Model-1'].rootAssembly
a.LinearInstancePattern(instanceList=('Down support-1', ), direction1=(1.0, 
    0.0, 0.0), direction2=(0.0, 1.0, 0.0), number1=1, number2=2, spacing1=0.2, 
    spacing2=0.0204999)


a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Down support-1-lin-1-2', ), vector=(0.0, -0.0205, 
    2.95))
#: The instance Down support-1-lin-1-2 was translated by 0., -20.5E-03, 2.95 with respect to the assembly coordinate system

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Down rebar']
a.Instance(name='Down rebar-1', part=p, dependent=ON)


a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('Down rebar-1', ), axisPoint=(-0.1, 0.2, 0.0), 
    axisDirection=(0.0, -0.359, 0.0), angle=90.0)
#: The instance Down rebar-1 was rotated by 90. degrees about the axis defined by the point -100.E-03, 200.E-03, 0. and the vector 0., -359.E-03, 0.
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Down rebar-1', ), vector=(0.0, -0.159, -0.1))
#: The instance Down rebar-1 was translated by 0., -159.E-03, -100.E-03 with respect to the assembly coordinate system

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Down rebar-1', ), vector=(0.041, 0.0, 0.0))
#: The instance Down rebar-1 was translated by 41.E-03, 0., 0. with respect to the assembly coordinate system

a1 = mdb.models['Model-1'].rootAssembly
i1 = a1.instances['Concrete-1']
leaf = dgm.LeafFromInstance((i1, ))
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
    leaf=leaf)
leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.either(leaf=leaf)
a = mdb.models['Model-1'].rootAssembly
a.LinearInstancePattern(instanceList=('Down rebar-1', ), direction1=(1.0, 0.0, 
    0.0), direction2=(0.0, 1.0, 0.0), number1=2, number2=3, spacing1=1.0, 
    spacing2=0.02)

leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
    leaf=leaf)
a1 = mdb.models['Model-1'].rootAssembly
i1 = a1.instances['Concrete-1']
leaf = dgm.LeafFromInstance((i1, ))
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
    leaf=leaf)
a1 = mdb.models['Model-1'].rootAssembly
i1 = a1.instances['Concrete-1']
leaf = dgm.LeafFromInstance((i1, ))
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
    leaf=leaf)
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Down rebar-1-lin-1-3', ), vector=(-0.041, -0.04, 
    0.0))
#: The instance Down rebar-1-lin-1-3 was translated by -41.E-03, -40.E-03, 0. with respect to the assembly coordinate system
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Down rebar-1-lin-1-3', ), vector=(0.1, 0.0, 0.0))
#: The instance Down rebar-1-lin-1-3 was translated by 100.E-03, 0., 0. with respect to the assembly coordinate system
a1 = mdb.models['Model-1'].rootAssembly
i1 = a1.instances['Concrete-1']
leaf = dgm.LeafFromInstance((i1, ))
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
    leaf=leaf)
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Down rebar-1-lin-1-2', ), vector=(-0.041, -0.02, 
    0.0))
#: The instance Down rebar-1-lin-1-2 was translated by -41.E-03, -20.E-03, 0. with respect to the assembly coordinate system
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Down rebar-1-lin-1-2', ), vector=(0.159, 0.0, 0.0))
#: The instance Down rebar-1-lin-1-2 was translated by 159.E-03, 0., 0. with respect to the assembly coordinate system

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Up rebar']
a.Instance(name='Up rebar-1', part=p, dependent=ON)
a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('Up rebar-1', ), axisPoint=(0.0, 0.0, 0.0), 
    axisDirection=(0.0, 0.2, 0.0), angle=90.0)
#: The instance Up rebar-1 was rotated by 90. degrees about the axis defined by the point 0., 0., 0. and the vector 0., 200.E-03, 0.

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Up rebar-1', ), vector=(-0.1, 0.159, 1.0))
#: The instance Up rebar-1 was translated by -100.E-03, 159.E-03, 1. with respect to the assembly coordinate system

a = mdb.models['Model-1'].rootAssembly
a.LinearInstancePattern(instanceList=('Up rebar-1', ), direction1=(1.0, 0.0, 
    0.0), direction2=(0.0, 1.0, 0.0), number1=1, number2=4, spacing1=1.0, 
    spacing2=0.1)
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Up rebar-1', ), vector=(0.159, 0.0, 0.0))
#: The instance Up rebar-1 was translated by 159.E-03, 0., 0. with respect to the assembly coordinate system
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Up rebar-1-lin-1-2', ), vector=(0.0, -0.1, 0.0))
#: The instance Up rebar-1-lin-1-2 was translated by 0., -100.E-03, 0. with respect to the assembly coordinate system
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Up rebar-1-lin-1-2', ), vector=(0.041, 0.0, 0.0))
#: The instance Up rebar-1-lin-1-2 was translated by 41.E-03, 0., 0. with respect to the assembly coordinate system

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Up rebar-1-lin-1-3', ), vector=(0.0, -0.2, 2.0))
#: The instance Up rebar-1-lin-1-3 was translated by 0., -200.E-03, 2. with respect to the assembly coordinate system
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Up rebar-1-lin-1-3', ), vector=(0.159, 0.0, 0.0))
#: The instance Up rebar-1-lin-1-3 was translated by 159.E-03, 0., 0. with respect to the assembly coordinate system
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Up rebar-1-lin-1-4', ), vector=(0.0, -0.3, 2.0))
#: The instance Up rebar-1-lin-1-4 was translated by 0., -300.E-03, 2. with respect to the assembly coordinate system
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Up rebar-1-lin-1-4', ), vector=(0.041, 0.0, 0.0))
#: The instance Up rebar-1-lin-1-4 was translated by 41.E-03, 0., 0. with respect to the assembly coordinate system

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Constrain rebar']
a.Instance(name='Constrain rebar-1', part=p, dependent=ON)

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Constrain rebar-1', ), vector=(0.0, 0.0, 0.02))
#: The instance Constrain rebar-1 was translated by 0., 0., 20.E-03 with respect to the assembly coordinate system

  


a = mdb.models['Model-1'].rootAssembly
a.rotate(instanceList=('Concrete-1', 'up support-1', 'up support-1-lin-1-2', 
    'Down support-1', 'Down support-1-lin-1-2', 'Down rebar-1', 
    'Down rebar-1-lin-1-2', 'Down rebar-1-lin-1-3', 'Down rebar-1-lin-2-1', 
    'Down rebar-1-lin-2-2', 'Down rebar-1-lin-2-3', 'Up rebar-1', 
    'Up rebar-1-lin-1-2', 'Up rebar-1-lin-1-3', 'Up rebar-1-lin-1-4', 
    'Constrain rebar-1'), axisPoint=(-0.1, -0.2, 0.0), axisDirection=(0.0, 0.4, 
    0.0), angle=90.0)
#: The instances were rotated by 90. degrees about the axis defined by the point -100.E-03, -200.E-03, 0. and the vector 0., 400.E-03, 0.


a1 = mdb.models['Model-1'].rootAssembly
i1 = a1.instances['Concrete-1']
leaf = dgm.LeafFromInstance((i1, ))
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
a = mdb.models['Model-1'].rootAssembly
a.LinearInstancePattern(instanceList=('Constrain rebar-1', ), direction1=(1.0, 
    0.0, 0.0), direction2=(0.0, -1.0, 0.0), number1=8, number2=1, 
    spacing1=0.15, spacing2=0.373)


a1 = mdb.models['Model-1'].rootAssembly
del a1.features['Constrain rebar-1-lin-8-1']

a1 = mdb.models['Model-1'].rootAssembly
c1 = a1.instances['Concrete-1'].cells


a1 = mdb.models['Model-1'].rootAssembly
a1.deleteFeatures(('Down rebar-1-lin-2-1', 'Down rebar-1-lin-2-2', 
    'Down rebar-1-lin-2-3', ))
a1 = mdb.models['Model-1'].rootAssembly
c1 = a1.instances['Concrete-1'].cells

 
p1 = mdb.models['Model-1'].parts['up support']



a = mdb.models['Model-1'].rootAssembly
a.LinearInstancePattern(instanceList=('Constrain rebar-1-lin-7-1', ), 
    direction1=(1.0, 0.0, 0.0), direction2=(0.0, -1.0, 0.0), number1=2, 
    number2=1, spacing1=0.15, spacing2=0.373)

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Constrain rebar-1-lin-7-1-lin-2-1', ), vector=(1.93, 
    -0.0275, -0.0275))
#: The instance Constrain rebar-1-lin-7-1-lin-2-1 was translated by 1.93, -27.5E-03, -27.5E-03 with respect to the assembly coordinate system

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Constrain rebar-1-lin-7-1-lin-2-1', ), vector=(0.0, 
    0.014, 0.0))
#: The instance Constrain rebar-1-lin-7-1-lin-2-1 was translated by 0., 14.E-03, 0. with respect to the assembly coordinate system

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Constrain rebar-1-lin-7-1-lin-2-1', ), vector=(0.0, 
    0.0, 0.014))
#: The instance Constrain rebar-1-lin-7-1-lin-2-1 was translated by 0., 0., 14.E-03 with respect to the assembly coordinate system
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Constrain rebar-1-lin-7-1-lin-2-1', ), vector=(0.0, 
    0.0, 0.014))
#: The instance Constrain rebar-1-lin-7-1-lin-2-1 was translated by 0., 0., 14.E-03 with respect to the assembly coordinate system

a1 = mdb.models['Model-1'].rootAssembly
del a1.features['Constrain rebar-1-lin-7-1-lin-2-1']

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Constrain rebar']
a.Instance(name='Constrain rebar-2', part=p, dependent=ON)

a1 = mdb.models['Model-1'].rootAssembly
del a1.features['Constrain rebar-2']
a = mdb.models['Model-1'].rootAssembly
a.LinearInstancePattern(instanceList=('Constrain rebar-1', ), direction1=(1.0, 
    0.0, 0.0), direction2=(0.0, -1.0, 0.0), number1=2, number2=1, 
    spacing1=2.98, spacing2=0.373)
 

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Constrain rebar-1-lin-2-1-1', ), vector=(-0.02, 0.0, 
    0.0))
#: The instance Constrain rebar-1-lin-2-1-1 was translated by -20.E-03, 0., 0. with respect to the assembly coordinate system
a1 = mdb.models['Model-1'].rootAssembly
i1 = a1.instances['Concrete-1']
leaf = dgm.LeafFromInstance((i1, ))
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
session.viewports['Viewport: 1'].view.setValues(nearPlane=5.17902, 
    cameraPosition=(6.3061, 0.924091, -4.32051), cameraUpVector=(-0.0773748, 
    0.986026, 0.147532), cameraTarget=(1.47041, -0.0700998, -0.212007))
leaf = dgm.Leaf(leafType=DEFAULT_MODEL)


a1 = mdb.models['Model-1'].rootAssembly
c1 = a1.instances['Concrete-1'].cells
cells1 = c1.getSequenceFromMask(mask=('[#5 ]', ), )
leaf = dgm.LeafFromGeometry(cellSeq=cells1)

a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Constrain rebar-1-lin-2-1-1', ), vector=(-1.05, 0.0, 
    0.0))
#: The instance Constrain rebar-1-lin-2-1-1 was translated by -1.05, 0., 0. with respect to the assembly coordinate system
a1 = mdb.models['Model-1'].rootAssembly
c1 = a1.instances['Concrete-1'].cells
cells1 = c1.getSequenceFromMask(mask=('[#20 ]', ), )
leaf = dgm.LeafFromGeometry(cellSeq=cells1)
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
a = mdb.models['Model-1'].rootAssembly
a.LinearInstancePattern(instanceList=('Constrain rebar-1-lin-2-1-1', ), 
    direction1=(1.0, 0.0, 0.0), direction2=(0.0, -1.0, 0.0), number1=8, 
    number2=1, spacing1=0.15, spacing2=0.373)
a1 = mdb.models['Model-1'].rootAssembly
del a1.features['Constrain rebar-1-lin-2-1-1']



leaf = dgm.Leaf(leafType=DEFAULT_MODEL)

mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial', 
    description='load', initialInc=0.05, maxInc=0.1)

###Contact
mdb.models['Model-1'].ContactProperty('Contact')
mdb.models['Model-1'].interactionProperties['Contact'].NormalBehavior(
    pressureOverclosure=HARD, allowSeparation=ON, 
    constraintEnforcementMethod=DEFAULT)
a1 = mdb.models['Model-1'].rootAssembly
s1 = a1.instances['Concrete-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#4000000 ]', ), )
region1=a1.Surface(side1Faces=side1Faces1, name='contact-down1')
a1 = mdb.models['Model-1'].rootAssembly
s1 = a1.instances['Down support-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#3 ]', ), )
region2=a1.Surface(side1Faces=side1Faces1, name='contact-down1s')
mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='down1', 
    createStepName='Initial', master=region2, slave=region1, sliding=FINITE, 
    thickness=ON, interactionProperty='Contact', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

a1 = mdb.models['Model-1'].rootAssembly
s1 = a1.instances['Concrete-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#2 ]', ), )
region1=a1.Surface(side1Faces=side1Faces1, name='contact-down2')
a1 = mdb.models['Model-1'].rootAssembly
s1 = a1.instances['Down support-1-lin-1-2'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#3 ]', ), )
region2=a1.Surface(side1Faces=side1Faces1, name='contact-down2s')
mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='down2', 
    createStepName='Initial', master=region2, slave=region1, sliding=FINITE, 
    thickness=ON, interactionProperty='Contact', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

a1 = mdb.models['Model-1'].rootAssembly
s1 = a1.instances['Concrete-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#10000000 ]', ), )
region1=a1.Surface(side1Faces=side1Faces1, name='contact-up1')
a1 = mdb.models['Model-1'].rootAssembly
s1 = a1.instances['up support-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
region2=a1.Surface(side1Faces=side1Faces1, name='contact-up1s')
mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='up1', 
    createStepName='Initial', master=region2, slave=region1, sliding=FINITE, 
    thickness=ON, interactionProperty='Contact', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)

a1 = mdb.models['Model-1'].rootAssembly
s1 = a1.instances['Concrete-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#10000 ]', ), )
region1=a1.Surface(side1Faces=side1Faces1, name='contact-up2')
a1 = mdb.models['Model-1'].rootAssembly
s1 = a1.instances['up support-1-lin-1-2'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#1 ]', ), )
region2=a1.Surface(side1Faces=side1Faces1, name='contact-up2s')
mdb.models['Model-1'].SurfaceToSurfaceContactStd(name='up2', 
    createStepName='Initial', master=region2, slave=region1, sliding=FINITE, 
    thickness=ON, interactionProperty='Contact', adjustMethod=NONE, 
    initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
### contacet end 





###embedded
a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['Down rebar-1'].edges
edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )
e2 = a.instances['Down rebar-1-lin-1-2'].edges
edges2 = e2.getSequenceFromMask(mask=('[#1 ]', ), )
e3 = a.instances['Down rebar-1-lin-1-3'].edges
edges3 = e3.getSequenceFromMask(mask=('[#1 ]', ), )
e4 = a.instances['Up rebar-1'].edges
edges4 = e4.getSequenceFromMask(mask=('[#1 ]', ), )
e5 = a.instances['Up rebar-1-lin-1-2'].edges
edges5 = e5.getSequenceFromMask(mask=('[#1 ]', ), )
e6 = a.instances['Up rebar-1-lin-1-3'].edges
edges6 = e6.getSequenceFromMask(mask=('[#1 ]', ), )
e7 = a.instances['Up rebar-1-lin-1-4'].edges
edges7 = e7.getSequenceFromMask(mask=('[#1 ]', ), )
e8 = a.instances['Constrain rebar-1'].edges
edges8 = e8.getSequenceFromMask(mask=('[#f ]', ), )
e9 = a.instances['Constrain rebar-1-lin-2-1'].edges
edges9 = e9.getSequenceFromMask(mask=('[#f ]', ), )
e10 = a.instances['Constrain rebar-1-lin-3-1'].edges
edges10 = e10.getSequenceFromMask(mask=('[#f ]', ), )
e11 = a.instances['Constrain rebar-1-lin-4-1'].edges
edges11 = e11.getSequenceFromMask(mask=('[#f ]', ), )
e12 = a.instances['Constrain rebar-1-lin-5-1'].edges
edges12 = e12.getSequenceFromMask(mask=('[#f ]', ), )
e13 = a.instances['Constrain rebar-1-lin-6-1'].edges
edges13 = e13.getSequenceFromMask(mask=('[#f ]', ), )
e14 = a.instances['Constrain rebar-1-lin-7-1'].edges
edges14 = e14.getSequenceFromMask(mask=('[#f ]', ), )
e15 = a.instances['Constrain rebar-1-lin-2-1-1-lin-2-1'].edges
edges15 = e15.getSequenceFromMask(mask=('[#f ]', ), )
e16 = a.instances['Constrain rebar-1-lin-2-1-1-lin-3-1'].edges
edges16 = e16.getSequenceFromMask(mask=('[#f ]', ), )
e17 = a.instances['Constrain rebar-1-lin-2-1-1-lin-4-1'].edges
edges17 = e17.getSequenceFromMask(mask=('[#f ]', ), )
e18 = a.instances['Constrain rebar-1-lin-2-1-1-lin-5-1'].edges
edges18 = e18.getSequenceFromMask(mask=('[#f ]', ), )
e19 = a.instances['Constrain rebar-1-lin-2-1-1-lin-6-1'].edges
edges19 = e19.getSequenceFromMask(mask=('[#f ]', ), )
e20 = a.instances['Constrain rebar-1-lin-2-1-1-lin-7-1'].edges
edges20 = e20.getSequenceFromMask(mask=('[#f ]', ), )
e21 = a.instances['Constrain rebar-1-lin-2-1-1-lin-8-1'].edges
edges21 = e21.getSequenceFromMask(mask=('[#f ]', ), )
region1=a.Set(edges=edges1+edges2+edges3+edges4+edges5+edges6+edges7+edges8+\
    edges9+edges10+edges11+edges12+edges13+edges14+edges15+edges16+edges17+\
    edges18+edges19+edges20+edges21, name='slave')
a = mdb.models['Model-1'].rootAssembly
c1 = a.instances['Concrete-1'].cells
cells1 = c1.getSequenceFromMask(mask=('[#7f ]', ), )
region2=a.Set(cells=cells1, name='host')
mdb.models['Model-1'].EmbeddedRegion(name='embeded', embeddedRegion=region1, 
    hostRegion=region2, weightFactorTolerance=1e-06, absoluteTolerance=0.0, 
    fractionalTolerance=0.05, toleranceMethod=BOTH)
### end embedded

### Boundry condition
p = mdb.models['Model-1'].parts['Down support']
e = p.edges
p.DatumPointByMidPoint(point1=p.InterestingPoint(edge=e[1], rule=MIDDLE), 
    point2=p.InterestingPoint(edge=e[3], rule=MIDDLE))
p = mdb.models['Model-1'].parts['Down support']
v1, e1, d1, n1 = p.vertices, p.edges, p.datums, p.nodes
p.ReferencePoint(point=d1[2])
a = mdb.models['Model-1'].rootAssembly
a.regenerate()


a1 = mdb.models['Model-1'].rootAssembly
r1 = a1.instances['Down support-1-lin-1-2'].referencePoints
refPoints1=(r1[3], )
region = a1.Set(referencePoints=refPoints1, name='Set-3')
mdb.models['Model-1'].DisplacementBC(name='downFIx1', createStepName='Initial', 
    region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)
r1 = a1.instances['Down support-1'].referencePoints
refPoints1=(r1[3], )
region = a1.Set(referencePoints=refPoints1, name='Set-2')
mdb.models['Model-1'].DisplacementBC(name='downFIx2', createStepName='Initial', 
    region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

a1 = mdb.models['Model-1'].rootAssembly
r1 = a1.instances['up support-1'].referencePoints
refPoints1=(r1[3], )
r2 = a1.instances['up support-1-lin-1-2'].referencePoints
refPoints2=(r2[3], )
region = a1.Set(referencePoints=(refPoints1, refPoints2, ), name='Set-4')
mdb.models['Model-1'].DisplacementBC(name='upload', createStepName='Step-1',  ###canBeParalized  u2
    region=region, u1=UNSET, u2=-0.005, u3=UNSET, ur1=UNSET, ur2=UNSET, 
    ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, 
    fieldName='', localCsys=None)
### BC end

### mesh
p = mdb.models['Model-1'].parts['Concrete']
p.seedPart(size=0.01, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['Concrete']
p.generateMesh()
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
c = p.cells
cells = c.getSequenceFromMask(mask=('[#7f ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))


p = mdb.models['Model-1'].parts['Constrain rebar']
p.seedPart(size=0.037, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()
elemType1 = mesh.ElemType(elemCode=T3D2, elemLibrary=STANDARD)
e = p.edges
edges = e.getSequenceFromMask(mask=('[#f ]', ), )
pickedRegions =(edges, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))



p = mdb.models['Model-1'].parts['Down rebar']
p.seedPart(size=0.05, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()
e = p.edges
edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =(edges, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))



p = mdb.models['Model-1'].parts['Up rebar']
p.seedPart(size=0.05, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()
e = p.edges
edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =(edges, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

a = mdb.models['Model-1'].rootAssembly
a.regenerate()

###end mesh


###output file
mdb.models['Model-1'].FieldOutputRequest(name='usrdefine', 
    createStepName='Step-1', variables=('PEEQ', 'PEEQT', 'PEEQMAX', 'PEMAG'))
a1 = mdb.models['Model-1'].rootAssembly
r1 = a1.instances['up support-1'].referencePoints
refPoints1=(r1[3], )
a1.Set(referencePoints=refPoints1, name='up1')
#: The set 'up1' has been created (1 reference point).
a1 = mdb.models['Model-1'].rootAssembly
r1 = a1.instances['up support-1-lin-1-2'].referencePoints
refPoints1=(r1[3], )
a1.Set(referencePoints=refPoints1, name='up2')
#: The set 'up2' has been created (1 reference point).
regionDef=mdb.models['Model-1'].rootAssembly.sets['up1']
mdb.models['Model-1'].HistoryOutputRequest(name='up load', 
    createStepName='Step-1', variables=('IRF1', 'IRF2', 'IRF3'), 
    region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)
regionDef=mdb.models['Model-1'].rootAssembly.sets['up2']
mdb.models['Model-1'].HistoryOutputRequest(name='up load 2', 
    createStepName='Step-1', variables=('RF1', 'RF2', 'RF3'), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)
mdb.models['Model-1'].historyOutputRequests['up load'].setValues(variables=(
    'RF1', 'RF2', 'RF3'))

###end output file

mdb.Job(name='model1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=2, numDomains=2, 
    numGPUs=0)

session.viewports['Viewport: 1'].view.setValues(session.views['Back'])
session.viewports['Viewport: 1'].assemblyDisplay.setValues(renderStyle=SHADED)
leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
    leaf=leaf)