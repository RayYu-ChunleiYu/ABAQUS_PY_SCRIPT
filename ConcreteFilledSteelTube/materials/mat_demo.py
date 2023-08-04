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
from materials import uhpc_ca_steelFiber_abaqus_param_usdfd
# from .pyScript.modelMaterials.materials import *

model_name = 'Model-1'
fc0 = 117
Vca= 0
Vs = 0.03
lds = 60
material_name = "zengyanqing"

# model create 


# tube part
current_model = mdb.models[model_name]

concrete_para_dict = uhpc_ca_steelFiber_abaqus_param_usdfd(fc0,Vca,Vs,lds)
current_model.Material(name=material_name)
current_model.materials[material_name].UserDefinedField()

current_model.materials[material_name].Density(table=concrete_para_dict['Density'])
current_model.materials[material_name].Elastic(table=concrete_para_dict['Elastic'])

current_model.materials[material_name].ConcreteDamagedPlasticity(
    dependencies=3,
    table=concrete_para_dict['CDP']
    )
current_model.materials[material_name].concreteDamagedPlasticity.ConcreteCompressionHardening(
    dependencies=1,
    table=concrete_para_dict['CompressionHardening']
    )
current_model.materials[material_name].concreteDamagedPlasticity.ConcreteCompressionDamage(
    dependencies=1,
    table=concrete_para_dict['CompressionDamage']
    )
current_model.materials[material_name].concreteDamagedPlasticity.ConcreteTensionStiffening(
    table=concrete_para_dict['TensionStiffening'])
current_model.materials[material_name].concreteDamagedPlasticity.ConcreteTensionDamage(
    table=concrete_para_dict['TensionDamage'])
current_model.materials[material_name].Depvar()
current_model.materials[material_name].depvar.setValues(n=20)
