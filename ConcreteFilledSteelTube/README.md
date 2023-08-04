# An Abqus batch process script for analysis CFST 

## Task usage
### Defination
Every task in aimd at one load_pattern of CFST, run the task to launch correspond abaqus FEM analysis

### Example script
Seen in task_analysis.py

## Controller usage 
### Defination
A controller can add lots of task and to run them parallelly

### Example script
Seen in controller_anlayais.py 

## Implement tasks

### bending tasks
- bendingAnlysisWithOnePinAndOnexyConstrainSupport_Circle_Section  -------- TaskBendingCircleFixUnsymmetry
- bendingAnlysisWithTwoxyConstrainSupport_Circle_section -------- TaskBendingCircleFixSymmetry
- bendingAnlysisWithTwoxyConstrainSupport_rectangle_section -------- TaskBendingRectFixSymmetry
- bendingAnlysisWithTwoxyConstrainSupportAndPlateEdgeZConstrain_Circle_section  --------   TaskBendingCircleFixUnsymmetryOnePlateEdgeFix

### tension tasks
- TaskTensionCircle  -------- TaskTensionCircle
- TaskTensionRect  -------- TaskTensionRect








