# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2022 replay file
# Internal Version: 2021_09_16-01.57.30 176069
# Run by YCL on Wed Mar  1 16:29:04 2023

import numpy as np 
import scipy.optimize as op


def steelBialinear(fy):
    '''input fy of steel and return material parameters using in abaqus'''
    E = 2.1 * 100000
    epsilon0 = fy / E
    Et = E * 0.01
    elasticPara = ((0, 0), (epsilon0, fy))
    hardeningPara = ((0.15 + epsilon0, fy + Et * 0.15), (0, 0))
    ###output data
    youngsModulus = E
    possionsRatio = 0.30
    plasticPara = ((elasticPara[1][1], 0), (hardeningPara[0][1], hardeningPara[0][0] - hardeningPara[0][1] / E))
    # self.steel={'elastic':(youngsModulus,possionsRatio),'Plastic':plasticPara}
    return {
        "Density": ((7.85E-6,),),
        'Elastic': (youngsModulus, possionsRatio),
        'Plastic': plasticPara
    }


def steelYieldAndHarding(fy):
    E = 2.1 * 100000
    epsilon_e = 0.8 * fy / E
    epsilon_s1 = 1.5 * epsilon_e
    epsilon_s2 = 10 * epsilon_e
    epsilon_s3 = 100 * epsilon_e

    fu = 1.42 * fy

    plastic_para = ((0.8 * fy, 0), (fy, epsilon_s1 - fy / E), (fy, epsilon_s2 - fy / E), (fu, epsilon_s3 - fu / E))

    return {
        "Density": ((7.85E-6,),),
        'Elastic': (E, 0.3),
        'Plastic': plastic_para
    }


def plateRigid():
    '''input fy of steel and return material parameters using in abaqus'''
    fy = 10000  # 10000 Mpa
    E = 2.1 * 1000000  # 2100 Gpa
    epsilon0 = fy / E
    Et = E * 0.01
    elasticPara = ((0, 0), (epsilon0, fy))
    hardeningPara = ((0.15 + epsilon0, fy + Et * (0.15 + epsilon0 - epsilon0)), (0, 0))
    ###output data
    youngsModulus = E
    possionsRatio = 0.30
    plasticPara = ((elasticPara[1][1], 0), (hardeningPara[0][1], hardeningPara[0][0] - hardeningPara[0][1] / E))
    # self.steel={'elastic':(youngsModulus,possionsRatio),'Plastic':plasticPara}
    return {
        "Density": ((7.85E-6,),),
        'Elastic': (youngsModulus, possionsRatio),
        'Plastic': plasticPara
    }


def concrete():
    return {
        "Density": ((2.5E-6,),),
        "Elastic": ((48205.4624646717, 0.2),),
        "CDP": ((38.0, 0.1, 1.16, 0.66667, 0.0005),),
        "CompressionHardening": ((43.573047619618, 0.0), (107.174982043751, 0.000488412715309141), (
            109.000744514366, 0.000751839017779118), (79.7566423275852,
                                                      0.00196109617701872), (38.4708510050705, 0.00372145350175807), (
                                     16.7693453099025, 0.00567814568777312), (6.95749433070424,
                                                                              0.00889469698957272),
                                 (4.23303862191714, 0.0119642235579076)),
        "TensionStiffening": ((9.54233223228928, 0.0),),
        "CompressionDamage": ((0.0, 0.0), (0.0945236449009135, 0.000488412715309141), (
            0.13370383635158, 0.000751839017779118), (0.323536346066794,
                                                      0.00196109617701872), (0.579784636965906, 0.00372145350175807), (
                                  0.759732674017529, 0.00567814568777312), (0.873637717454765,
                                                                            0.00889469698957272),
                              (0.914641302639581, 0.0119642235579076))
    }


def cohesive():
    return {
        "Density": ((2E-6,),),
        'QuadsDamage': ((2.6, 10.0, 10.0),),
        'DamageEvolution': ((0.025, 0.625, 0.625),),
        'ElasticTraction': ((100000.0, 1000000.0, 1000000.0),),

    }


def cohesiveConcreteTension():
    return {
        "Density": ((2.5E-6,),),
        'QuadsDamage': ((6.0, 10.0, 10.0),),
        'DamageEvolution': ((0.003, 0.625, 0.625),),
        'ElasticTraction': ((60000.0, 1000000.0, 1000000.0),),
    }


def concreteInstandreofChina(fcu):
    if fcu <= 50.0:
        alphac1 = 0.76
    elif 50.0 < fcu <= 80.0:
        alphac1 = 0.76 + (fcu - 50) * (0.82 - 0.76) / (80 - 50)
    else:
        alphac1 = 0.82
    if fcu <= 40:
        alphac2 = 1
    elif 40.0 < fcu <= 80.0:
        alphac2 = 1 + (fcu - 40) * (0.87 - 1) / (80 - 40)
    else:
        alphac2 = 0.87
    if fcu == 15.0:
        deviationConstant = 0.21
    elif fcu == 20.0:
        deviationConstant = 0.18
    elif fcu == 25.0:
        deviationConstant = 0.16
    elif fcu == 30.0:
        deviationConstant = 0.14
    elif fcu == 35.0:
        deviationConstant = 0.13
    elif fcu <= 45.0:
        deviationConstant = 0.12
    elif fcu <= 55.0:
        deviationConstant = 0.11
    elif fcu >= 80.0:
        deviationConstant = 0.10
    ftk = 0.88 * 0.395 * fcu ** 0.55 * alphac2 * (1 - 1.645 * deviationConstant) ** 0.45
    fck = fcu * alphac1 * alphac2 * 0.88
    Ec = 100000 / (2.2 + 34.7 / fcu)
    epsilonc = (700 + 172 * (fck) ** (0.5)) * 0.000001
    epsilont = (65 * ftk ** 0.54) * 0.000001
    compressionCurveParaPc = fck / Ec / epsilonc
    compressionCurveParaN = 1 / (1 - compressionCurveParaPc)
    compressionCurveAlphac = 0.157 * fck ** 0.785 - 0.905
    elasticStrainRatio = 0.0021 * fck + 0.1
    elasticStrain = elasticStrainRatio * epsilonc
    elasticStress = 1000000 * (compressionCurveParaN * (elasticStrain / epsilonc) / (
                compressionCurveParaN - 1 + (elasticStrain / epsilonc) ** compressionCurveParaN)) * fck
    youngsModulus = elasticStress / elasticStrain
    tensionCurveParaPt = ftk / Ec / epsilont
    tensionCurveParaN = 1 / (1 - tensionCurveParaPt)
    tensionCurveParaAlphat = 0.312 * ftk ** 2
    elasticStrainTensionRatio = (tensionCurveParaPt * tensionCurveParaN / (
                youngsModulus / 1000000 / Ec) - tensionCurveParaN + 1) ** (1 / tensionCurveParaN)
    elasticStrainTension = elasticStrainTensionRatio * epsilont
    elasticStressTension = 1000000 * (tensionCurveParaPt * tensionCurveParaN / (
                tensionCurveParaN - 1 + elasticStrainTensionRatio ** tensionCurveParaN)) * Ec * elasticStrainTensionRatio * epsilont
    epsiloncu = epsilonc * (1 + 2 * compressionCurveAlphac + (1 + 4 * compressionCurveAlphac) ** 0.5) / (
                2 * compressionCurveAlphac) * 1.7
    epsilontu = epsilont * (1 + 2 * tensionCurveParaAlphat + (1 + 4 * tensionCurveParaAlphat) ** 0.5) / (
                2 * tensionCurveParaAlphat) * 2

    ##data output zone
    elasticPara = (youngsModulus, 0.2)
    CDPPara = (40, 0.1, 1.225, 0.667, 0)
    TensileBehaviorGFI = (ftk * 1000000, 40 + (fck - 20) * (120 - 40) / (40 - 20))
    TensilebehaviorOther = (ftk * 1000000, 0)
    ##compression
    CompressionBehavior, CompressionDamage = [], []
    for i in range(0, 38):
        compressionStrain = elasticStrain + i * (epsilonc - elasticStrain) / 8
        compressionX = compressionStrain / epsilonc
        if compressionX <= 1:
            compressionStrain = elasticStrain + i * (epsilonc - elasticStrain) / 8
            compressionX = compressionStrain / epsilonc
            compressionY = compressionCurveParaN * compressionX / (
                        compressionCurveParaN - 1 + compressionX ** compressionCurveParaN)
        else:
            compressionStrain = epsilonc + (i - 8) * (epsiloncu - epsilonc) / 10
            compressionX = compressionStrain / epsilonc
            compressionY = compressionX / (compressionCurveAlphac * (compressionX - 1) ** 2 + compressionX)
        compressionStress = compressionY * fck * 1000000
        compressionInelasticStrain = compressionStrain - compressionStress / youngsModulus
        compressionYieldStress = compressionStress
        compressionDamageFactorMiddle = 1 - compressionStress / compressionStrain / youngsModulus
        compressionAdditionStrain = epsilonc / (epsilonc + compressionStrain) * (epsilonc * compressionStrain) ** 0.5
        compressionDamageFactorUsed = compressionStrain / (
                    compressionStrain + compressionAdditionStrain) * compressionDamageFactorMiddle
        CompressionDamage.append((compressionDamageFactorUsed, compressionInelasticStrain))
        CompressionBehavior.append((compressionYieldStress, compressionInelasticStrain))
    CompressionDamage.pop(0)
    CompressionDamage.insert(0, (0, 0))
    CompressionBehavior = tuple(CompressionBehavior)
    CompressionDamage = tuple(CompressionDamage)
    ##tension
    TensionBehavior, TensionDamage = [], []
    tensionXList = [0.41, 1, 1.5, 2, 3, 5, 7, 9, 11]
    ###
    # tensionStrain=elasticStrainTension
    # tensionX=tensionStrain/epsilont
    # if tensionX<=1:
    #     tensionY=(tensionCurveParaPt*tensionCurveParaN/(tensionCurveParaN-1+tensionX**tensionCurveParaN))*Ec*tensionX*epsilont/ftk
    # else:
    #     tensionY=(tensionCurveParaPt/(tensionCurveParaAlphat*(tensionX-1)**1.7+tensionX))*Ec*tensionX*epsilont/ftk
    # tensionStress=tensionY*ftk*1000000
    # tensionCrackStrain=tensionStrain-tensionStress/youngsModulus
    # TensionBehavior.append((tensionStress,tensionCrackStrain))
    for i, tensionX in enumerate(tensionXList):
        if tensionX <= 1:
            tensionY = (tensionCurveParaPt * tensionCurveParaN / (
                        tensionCurveParaN - 1 + tensionX ** tensionCurveParaN)) * Ec * tensionX * epsilont / ftk
            tensionStress = tensionY * ftk * 1000000
            tensionStrain = tensionX * epsilont
            tensionDamageUsed = 0
        else:
            tensionY = (tensionCurveParaPt / (
                        tensionCurveParaAlphat * (tensionX - 1) ** 1.7 + tensionX)) * Ec * tensionX * epsilont / ftk
            tensionStress = tensionY * ftk * 1000000
            tensionStrain = tensionX * epsilont
            tensionDamageUsed = 1 - tensionStress / (tensionStrain - (1 + (i + 8) * 0.01) * (
                        epsilont - ftk * 1000000 / youngsModulus)) / youngsModulus
            # tensionDamageUsed=1-tensionStress/(tensionStrain-(1+(i+1)*0.01)*(D$71-E$71/F$7))/F$7
        tensionCrackStrain = tensionStrain - tensionStress / youngsModulus
        TensionBehavior.append((tensionStress, tensionCrackStrain))
        TensionDamage.append((tensionDamageUsed, tensionCrackStrain))
    TensionStiffnessDisplacment = ((ftk * 1000000, 0), (0, epsilont))

    # error adjust first row
    TensionDamage.pop(0)
    TensionBehavior.pop(0)
    firstEpsilon = elasticStrainTension
    firstTensionX = firstEpsilon / epsilont
    firstTensionY = (tensionCurveParaPt * tensionCurveParaN / (
                tensionCurveParaN - 1 + firstTensionX ** tensionCurveParaN)) * Ec * firstTensionX * epsilont / ftk
    firstTensionStress = firstTensionY * ftk * 1000000
    TensionBehavior.insert(0, (firstTensionStress, 0))
    TensionDamage.insert(0, (0, 0))
    # soluted

    TensionBehavior = tuple(TensionBehavior)
    TensionDamage = tuple(TensionDamage)
    # self.concrete={'elastic':elasticPara,'CDP':CDPPara,'CompressionBehavior':CompressionBehavior,'TensileBehavior':TensionBehavior,
    #         'CompressionDamage':CompressionDamage,'TensileDamage':TensionDamage,'TensileBehaviorGFI':TensileBehaviorGFI,
    #         'TensileBehaviorDisplacement':TensionStiffnessDisplacment}  

    return {'Elastic': elasticPara, 'CDP': CDPPara, 'CompressionBehavior': CompressionBehavior,
            'TensileBehavior': TensionBehavior,
            'CompressionDamage': CompressionDamage, 'TensileDamage': TensionDamage,
            'TensileBehaviorGFI': TensileBehaviorGFI,
            'TensileBehaviorDisplacement': TensionStiffnessDisplacment}


def confinedUHPC(fcu, fy, Ac, As):
    if fcu <= 50:
        alpha1 = 0.76
    elif fcu >= 80:
        alpha1 = 0.82
    else:
        alpha1 = 0.76 + 0.002 * (fcu - 50)

    if fcu <= 40:
        alpha2 = 1
    elif fcu >= 80:
        alpha2 = 0.87
    else:
        alpha2 = 1 + 0.00325 * (40 - fcu)

    fc = 0.79 * fcu
    fck = 0.88 * alpha1 * alpha2 * fcu
    Ec = 4700 * fc ** 0.5
    ksi = As * fy / Ac / fck
    sigma0 = fc
    epsilonc = (1300 + 12.5 * fc) * 10 ** (-6)
    epsilon0 = epsilonc + 800 * (ksi ** 0.2) * (10 ** (-6))
    beta0 = (fc ** 0.1) / (1.2 * (1 + ksi) ** 0.5)
    concretestart = 0.3 * fc / Ec

    list2 = []
    for epsiloncc in np.arange(concretestart, concretestart + 25 * 0.0002, 0.0002):
        x = epsiloncc / epsilon0
        eta = 1.6 + 1.5 / x
        if x <= 1:
            y = 2 * x - x ** 2
        if x > 1:
            y = x / ((beta0 * ((x - 1) ** eta)) + x)
        sigmac = y * sigma0
        epsilonccc = epsiloncc - concretestart
        sigmac = float('%.2f' % sigmac)
        epsilonccc = float('%.6f' % epsilonccc)
        list2.append((sigmac * 1000000, epsilonccc))

    for epsiloncc in np.linspace(concretestart + 25 * 0.0002, 0.1, 0.0005):
        x = epsiloncc / epsilon0
        eta = 1.6 + 1.5 / x
        if x <= 1:
            y = 2 * x - x ** 2
        if x > 1:
            y = x / ((beta0 * ((x - 1) ** eta)) + x)
        sigmac = y * sigma0
        epsilonccc = epsiloncc - concretestart
        sigmac = float('%.2f' % sigmac)
        epsilonccc = float('%.6f' % epsilonccc)
        list2.append((sigmac * 1000000, epsilonccc))

    tuple2 = tuple(list2)

    sigmat0 = 0.26 * ((1.25 * fc) ** 0.666667)
    sigmat0 = float('%.3f' % sigmat0)
    if fcu == 20:
        gfi = 0.04
    elif fcu == 40:
        gfi = 0.12
    else:
        gfi = 0.004 * fcu - 0.04

    #  mm=> m UNITS
    # Ec = Ec * 1000000
    # sigmat0 = sigmat0 * 1000000
    # gfi = gfi * 1000
    return Ec, tuple2, sigmat0, gfi


def UHPCCA_with_confine_stress_compression_branch(fc,confine_stress=0,Vca=0.15,Vf=0.01,ascending_start_stress=0.82,ascending_point_num=10,decreasing_point_num= 30):
    """Stress-strain compression curve of UHPC-CA, considersing change of Vca and  Vs

    Args:
        fc (float): unconfiend peak stress. Unit Mpa
        confine_stress (float): activate confine stress.  Unit Mpa
        Vca (float): Volumn friction of corase aggregate. Unit 1
        Vf (float): Volumn friction of steel fibe. Unit 1
        ascending_point_num (int, optional): point num in ascending branch. Defaults to 10.
        decreasing_point_num (int, optional): point num in decreasing branch. Defaults to 40.

    Returns:
        tuple: (strain_list,stress_list)
        
        
    Reference:
    Yanqin Zeng - A refined finite element model tailored for predicting the compressive behaviors of FRP tube-confined UHPC-filled steel-encased column

    """
    
    E0 = 3980*fc**(0.5)
    epsilon0 = 0.75*fc**(0.31)
    epsilonCC = (1+ 11*confine_stress/fc)*epsilon0
    fcc = (1+18.18*confine_stress/fc)**(0.5)*fc
    
    
    lambda1 = 0.055/((confine_stress/fcc)+0.055)
    lambda2 = 0.017/((confine_stress/fcc)+0.017)
    
    n = lambda1*E0*epsilon0/1000/(E0*epsilon0/1000-fc)
    A = lambda2*(0.015*Vca*100-0.85*Vf*100+0.013*(fc-80)+3.99)
    
    ascending_function = lambda i : n*i/(n-1+i**n)-ascending_start_stress
    sloved_strain = op.fsolve(ascending_function,ascending_start_stress)
    
    ascending_strain_list = np.linspace(sloved_strain,1,ascending_point_num+1)
    decreasing_strain_list = np.linspace(1,5,decreasing_point_num+1)[1:]
    
    ascending_stress_list = [n*i/(n-1+i**n) for i in ascending_strain_list]
    
    decreasing_stress_list = [i/(A*(i-1)**2+i) for i in decreasing_strain_list]
    
    strain_list = list(ascending_strain_list)
    strain_list.extend(decreasing_strain_list)
    
    stress_list=  ascending_stress_list
    stress_list.extend(decreasing_stress_list)
    
    strain = [i*epsilonCC/1000 for i in strain_list]
    stress = [i*fcc for i in stress_list]
    
    damage = []
    for i,j in zip(strain,stress):
        if i > epsilonCC/1000:
            damage.append(1-j/fcc)
        else:
            damage.append(0)
    
    return  strain,stress,damage


def UHPC_CA_with_confine_compression_inelastic_transform_and_decimal_cut_off(fc,confine_stress=0,Vca=0.15,Vf=0.01,ascending_point_num=10,decreasing_point_num= 40):
    
    E0 = 3980*fc**(0.5)
    
    strain,stress,damage = UHPCCA_with_confine_stress_compression_branch(fc,confine_stress,Vca,Vf,0.8175,ascending_point_num,decreasing_point_num)
    
    strain,stress,damage = np.array(strain),np.array(stress),np.array(damage)
    
    plastic_strain = strain-stress/E0/(1-damage)
    plastic_stress = stress
    
    
    plastic_strain = np.around(plastic_strain,6)
    plastic_stress = np.around(plastic_stress,6)
    damage = np.around(damage,4)
    
    
    
    return plastic_strain,plastic_stress,damage
    

def UHPCCA_tension_branch(fct,fc,elastic_point_num=10,crack_smeared_point_num = 10,crack_localized_point_num=30):
    """Stress-strain tension curve of UHPC-CA, considersing change of Vca and  Vs

    Args:
        fct (float):  peak stress. Unit Mpa
        Vca (float): Volumn friction of corase aggregate. Unit 1
        Vf (float): Volumn friction of steel fibe. Unit 1
        elastic_point_num (int, optional): point num in ascending elastic branch. Defaults to 10.
        crack_smeared_point_num (int, optional): point num in decreasing crack smeared branch. Defaults to 10.
        crack_localized_point_num (int, optional): point num in decreasing crack localized branch. Defaults to 40.

    Returns:
        tuple: (strain_list,stress_list)
        
    Reference:
    Zhangchong Shi - Uniaxial tensile response and tensile constitutive model of ultra-high performance concrete containing coarse aggregate (CA-UHPC)
    
    """
    
    ## E prediction equation applied Zeng's works with compression, Seen in function above
    Ect = 3980.0*fc**(0.5)
    ect = fct/Ect
    
    ectr = 2500.0/1000000
    # The residual tensile strength fctr is approximately 10%–20% decrease of the tensilestrength fct. 
    fctr = 0.85*fct
    
    # \epsilon_ct,max 
    ectmax = 35000.0/1000000
    
    # elastic phase
    elastic_strain = np.linspace(0,ect,elastic_point_num+1)[1:]
    elastic_stress = elastic_strain*Ect
    
    # crack smeared
    crack_smeared_strain = np.linspace(ect,ectr,crack_smeared_point_num+1)[1:]
    crack_smeared_stress = fct+(fctr-fct)/(ectr-ect)*(crack_smeared_strain-ect)
    
    
    # crack localized
    crack_localized_strain = np.linspace(ectr,ectmax,crack_localized_point_num+1)[1:]

    crack_localized_stress = fctr*(1+(-1*(crack_localized_strain-ectr)/ectmax)**3)*np.exp(-4*(crack_localized_strain-ectr)/ectmax)
    
    return np.concatenate([elastic_strain,crack_smeared_strain,crack_localized_strain]),np.concatenate([elastic_stress,crack_smeared_stress,crack_localized_stress])
    #
    
    

def UHPC_CA_tension_inelastic_transform_and_decimal_cut_off(fct,fc,elastic_point_num=10,crack_smeared_point_num = 10,crack_localized_point_num=40):
    """Stress-strain tension curve of UHPC-CA, considersing change of Vca and  Vs

    Args:
        fct (float):  peak stress. Unit Mpa
        Vca (float): Volumn friction of corase aggregate. Unit 1
        Vf (float): Volumn friction of steel fibe. Unit 1
        elastic_point_num (int, optional): point num in ascending elastic branch. Defaults to 10.
        crack_smeared_point_num (int, optional): point num in decreasing crack smeared branch. Defaults to 10.
        crack_localized_point_num (int, optional): point num in decreasing crack localized branch. Defaults to 40.

    Returns:
        tuple: (plastic_strain,plastic_stress,damage)
        
    Reference:
    Zhangchong Shi - Uniaxial tensile response and tensile constitutive model of ultra-high performance concrete containing coarse aggregate (CA-UHPC)
    
    """
    E0 = 3980*fc**(0.5)
    
    strain,stress = UHPCCA_tension_branch(fct,fc,elastic_point_num,crack_smeared_point_num,crack_localized_point_num)
    # print("-----------------------------------------")
    # print(f"strain: {strain}")
    # print("-----------------------------------------")
    # print(f"stress: {stress}")
    
    strain,stress = np.array(strain),np.array(stress)
    
    plastic_strain = strain-stress/E0

    plastic_stress = stress
    
    peak_index = np.argmax(stress)
    damage = []
    for i in range(len(plastic_stress)):
        if i<= peak_index:
            damage.append(0)
        else:
            damage.append(1-plastic_stress[i]/fct)
    # print("-----------------------------------------")
    # print(f"damage: {damage}")        
    
    plastic_strain = np.around(plastic_strain,6)
    plastic_stress = np.around(plastic_stress,6)
    damage = np.around(damage,4)
    
    
    return plastic_strain,plastic_stress,damage
    
def cdp_prameters():
    """Plasticity parameters of CDP
    
    Reference:
    Zhangchong Shi - Uniaxial tensile response and tensile constitutive model of ultra-high performance concrete containing coarse aggregate (CA-UHPC)
    
    """
    return {
        "phi":54.0,
        "e":0.1,
        "fb0/fc0":1.07,
        "kc":0.666,
        "mu":0.0001,
    }



def abaqus_concrete_params(fc,ft,confine_stress=0):
    density = 2.5e-6
    elastic = (3980.0*fc**(0.5), 0.2)
    CDPDict = cdp_prameters()
    CDP = tuple((CDPDict['phi'], CDPDict['e'], CDPDict['fb0/fc0'], CDPDict['kc'], CDPDict['mu']))
    plastic_strain_compression,plastic_stress_compression,damage_compression = UHPC_CA_with_confine_compression_inelastic_transform_and_decimal_cut_off(fc,confine_stress,ascending_point_num=1,decreasing_point_num=25)
    plastic_strain_tension,plastic_stress_tension,damage_tension = UHPC_CA_tension_inelastic_transform_and_decimal_cut_off(ft,fc,elastic_point_num=1,crack_smeared_point_num=5,crack_localized_point_num=20)
    plastic_strain_compression[0]=0
    plastic_strain_tension[0]=0

    
    compression_hardening = tuple(((i,j) for i,j in zip(plastic_stress_compression,plastic_strain_compression)))
    tension_hardening = tuple(((i,j) for i,j in zip(plastic_stress_tension,plastic_strain_tension)))
    
    compression_damage = tuple(((i,j) for i,j in zip(damage_compression,plastic_strain_compression)))
    tension_damage = tuple(((i,j) for i,j in zip(damage_tension,plastic_strain_tension)))

    return {
        "Density":((density,),),
        "Elastic":(elastic, ),
        "CDP":(CDP, ),
        "CompressionHardening":(compression_hardening),
        "TensionStiffening":(tension_hardening),
        "CompressionDamage":(compression_damage),
        "TensionDamage":(tension_damage),
    }
    
    
    
def cdp_parameters_usdfd():
    table=((0.1, 0.1, 1.1, 0.501, 0.0005, 0.0, 0.1, 0.501), (5.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 5.0, 0.501), (10.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 10.0, 0.501), (15.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 15.0, 0.501), (20.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 20.0, 0.501), (25.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 25.0, 0.501), (30.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 30.0, 0.501), (35.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 35.0, 0.501), (40.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 40.0, 0.501), (45.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 45.0, 0.501), (50.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 50.0, 0.501), (56.0, 0.1, 1.1, 0.501, 0.0005, 0.0, 56.0, 0.501), (0.1, 0.1, 1.1, 0.6, 0.0005, 0.0, 0.1, 0.6), (5.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 5.0, 0.6), (10.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 10.0, 0.6), (15.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 15.0, 0.6), (20.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 20.0, 0.6), (25.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 25.0, 0.6), (30.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 30.0, 0.6), (35.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 35.0, 0.6), (40.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 40.0, 0.6), (45.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 45.0, 0.6), (50.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 50.0, 0.6), (56.0, 0.1, 1.1, 0.6, 0.0005, 0.0, 56.0, 0.6), (0.1, 0.1, 1.1, 0.7, 0.0005, 0.0, 0.1, 0.7), (5.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 5.0, 0.7), (10.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 10.0, 0.7), (15.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 15.0, 0.7), (20.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 20.0, 0.7), (25.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 25.0, 0.7), (30.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 30.0, 0.7), (35.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 35.0, 0.7), (40.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 40.0, 0.7), (45.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 45.0, 0.7), (50.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 50.0, 0.7), (56.0, 0.1, 1.1, 0.7, 0.0005, 0.0, 56.0, 0.7), (0.1, 0.1, 1.1, 0.8, 0.0005, 0.0, 0.1, 0.8), (5.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 5.0, 0.8), (10.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 10.0, 0.8), (15.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 15.0, 0.8), (20.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 20.0, 0.8), (25.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 25.0, 0.8), (30.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 30.0, 0.8), (35.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 35.0, 0.8), (40.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 40.0, 0.8), (45.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 45.0, 0.8), (50.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 50.0, 0.8), (56.0, 0.1, 1.1, 0.8, 0.0005, 0.0, 56.0, 0.8), (0.1, 0.1, 1.1, 0.9, 0.0005, 0.0, 0.1, 0.9), (5.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 5.0, 0.9), (10.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 10.0, 0.9), (15.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 15.0, 0.9), (20.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 20.0, 0.9), (25.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 25.0, 0.9), (30.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 30.0, 0.9), (35.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 35.0, 0.9), (40.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 40.0, 0.9), (45.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 45.0, 0.9), (50.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 50.0, 0.9), (56.0, 0.1, 1.1, 0.9, 0.0005, 0.0, 56.0, 0.9), (0.1, 0.1, 1.1, 1.0, 0.0005, 0.0, 0.1, 1.0), (5.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 5.0, 1.0), (10.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 10.0, 1.0), (15.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 15.0, 1.0), (20.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 20.0, 1.0), (25.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 25.0, 1.0), (30.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 30.0, 1.0), (35.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 35.0, 1.0), (40.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 40.0, 1.0), (45.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 45.0, 1.0), (50.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 50.0, 1.0), (56.0, 0.1, 1.1, 1.0, 0.0005, 0.0, 56.0, 1.0))
    return table
    
def uhpc_ca_steelFiber_abaqus_param_usdfd(fc0,Vca,Vs,lds):
    
    cdp_table = cdp_parameters_usdfd()
    
    
    sand_motar_with_fiber_compressive_strength = fc0+Vs*fc0*2.3
    
    density = 2.5e-6
    elastic = (round(3980.0*sand_motar_with_fiber_compressive_strength**(0.5),2), 0.2)
    
    sand_motar_with_fiber_tensile_strength = 4.82*np.log(Vs*lds)+9.08
    whole_compression_hardening = []
    whole_compression_damage = []
    
    
    
    for confine_stress in [0,5,10,15,20,25,30,35,40]:
        
        plastic_strain_compression,plastic_stress_compression,damage_compression = UHPC_CA_with_confine_compression_inelastic_transform_and_decimal_cut_off(sand_motar_with_fiber_compressive_strength,confine_stress,Vca,Vs,ascending_point_num=5,decreasing_point_num=20)
        plastic_strain_tension,plastic_stress_tension,damage_tension = UHPC_CA_tension_inelastic_transform_and_decimal_cut_off(sand_motar_with_fiber_tensile_strength,sand_motar_with_fiber_compressive_strength,elastic_point_num=1,crack_smeared_point_num=2,crack_localized_point_num=20)
        plastic_strain_compression = plastic_strain_compression-plastic_strain_compression[0]
        plastic_strain_tension[0]=0
        
        if confine_stress == 0 :
            unconfine_elastic_stress = plastic_stress_compression[0]
        
        plastic_stress_compression = plastic_stress_compression-plastic_stress_compression[0]+unconfine_elastic_stress
        
        [whole_compression_hardening.append((i,j,confine_stress)) for i,j in zip(plastic_stress_compression,plastic_strain_compression)]

        [whole_compression_damage.append((i,j,confine_stress)) for i,j in zip(damage_compression,plastic_strain_compression)]
        
        
    tension_hardening = [(i,j) for i,j in zip(plastic_stress_tension,plastic_strain_tension)]
    tension_damage = [(i,j) for i,j in zip(damage_tension,plastic_strain_tension)]
    
    
    return {
        "Density":((density,),),
        "Elastic":(elastic, ),
        "CDP":cdp_table,
        "CompressionHardening":(tuple(whole_compression_hardening)),
        "CompressionDamage":(tuple(whole_compression_damage)),
        "TensionStiffening":(tuple(tension_hardening)),
        "TensionDamage":(tuple(tension_damage)),
    }
    
    
    
    
    

    
    