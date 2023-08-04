# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2022 replay file
# Internal Version: 2021_09_16-01.57.30 176069
# Run by YCL on Thu Mar  2 10:29:21 2023

from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=140.869781494141, 
    height=103.511581420898)
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

o1 = session.openOdb(name=r'E:/YuChunlei/data_expand_FEM/bending_analysis.odb')

odb = session.odbs[r'E:/YuChunlei/data_expand_FEM/bending_analysis.odb']

session.viewports['Viewport: 1'].setValues(displayedObject=o1)

# displacement get data
displacment = session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('UT', NODAL, ((COMPONENT, 'UT3'), )), ), 
    nodeSets=("PLATE2_LOAD",))

# force get data
reaction_force = session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=(('RF', NODAL, ((COMPONENT, 'RF3'), )), ), 
    nodeSets=("PLATE2_LOAD",))

# steel strain get 
steel_strain = session.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT, 
    variable=(('E', INTEGRATION_POINT, ((COMPONENT, 'E33'), )), ), 
    elementSets=("INSTANCE_TUBE._G11", ))

# get max strain envelope
max_steel_strain = maxEnvelope(tuple(steel_strain))
max_steel_strain.setValues(sourceDescription='max_steel_strain')
session.xyDataObjects.changeKey(max_steel_strain.name, 'max_steel_strain')

# get min strain envelope
min_steel_strain = minEnvelope(tuple(steel_strain))
min_steel_strain.setValues(sourceDescription='min_steel_strain')
session.xyDataObjects.changeKey(min_steel_strain.name, 'min_steel_strain')


# displacement xydata process
displacment_1 = displacment[0]
displacment_1.setValues(sourceDescription='displacment')
session.xyDataObjects.changeKey(displacment_1.name, 'displacement')

# force xydata process

reaction_force2_sum = sum(tuple(reaction_force))
reaction_force2_sum.setValues(sourceDescription='reaction_force')
session.xyDataObjects.changeKey(reaction_force2_sum.name, 'reaction_force')

# # combine xy data
xy1 = session.xyDataObjects['displacement']
xy2 = session.xyDataObjects['reaction_force']
curve1 = combine(xy1, xy2)
curve1.setValues(sourceDescription='displacment_vs_reaction_force')
session.xyDataObjects.changeKey(curve1.name, 'displacment_vs_reaction_force')

## data export
x0 = session.xyDataObjects['displacment_vs_reaction_force']
session.writeXYReport(fileName='curve.txt', xyData=(x0, ))

x0 = session.xyDataObjects['max_steel_strain']
session.writeXYReport(fileName='max_steel_strain.txt', xyData=(x0, ))

x0 = session.xyDataObjects['min_steel_strain']
session.writeXYReport(fileName='min_steel_strain.txt', xyData=(x0, ))





