# -*- coding: utf-8 -*-

"""

ClosedLoopActuatorInMultiLayerMold_TwoMaterials.py

Ryan Truby, Harvard Lewis Research Group

2015.09.27

Library of mecode functions for printing soft robot pneunet actuators with three
independent sensors: a curvature, proprioceptive, and contact sensor.

"""


import os
import emb3DPGlobals
import emb3DMatrixPrinting
import CorrectedMultiMaterial 
import ClosedLoopActuatorSensors
import ClosedLoopActuator_ActuatorOnly

# Define the export file that will hold the generated G code
cur_filepath = os.path.dirname(os.path.realpath(__file__))
splitted = cur_filepath.split('/')
n = len(splitted)
cur_dir = ''.join((dir+'/') for dir in splitted[:n-1])
exportFileDir = cur_dir + "ClosedLoopActuatorinMultiLayerMold.pgm"
print "Exporting to file " + str(exportFileDir)

emb3DPGlobals.init_G(exportFileDir)

################################################################################
###
###    All actuator specific variables are in the actuator file.
###    All sensor specific variables are in the sensor file.
###    All mold specific and registration variables are in this file.   
###
################################################################################

# Set this for each print:
first_layer_bottom = -57.549            # This is the zero registration taken at the bottom of the the first mold layer
start_pos = [476.671, 129.511]                # This is the X, Y start coordinate, which should be +12 mm in X from the left most edge of the mold on it's midline
zero_on_curvature_sensor_matrix = -55.982    # added 2015.10.12, to get the exact height of the curature sensor matrix (wasn't getting good contact with this layer due to squeeging)

# Set these for each mold layer:
first_layer_thickness = 2.0      # Thickness of the layer for the curvature sensor, in mm
second_layer_thickness = 12.7       # Thickness of the layer for the actuator, in mm
third_layer_thickness = 3.0           # Thickness of the layer for the contact sensor, in mm
layer_width = 15
layer_length = 85

# The following can then be calculated:
true_second_layer_bottom = first_layer_bottom + first_layer_thickness # added 2015.10.12
second_layer_bottom = zero_on_curvature_sensor_matrix # added 2015.10.12
third_layer_bottom = true_second_layer_bottom + second_layer_thickness # added 2015.10.12
mold_top = third_layer_bottom + third_layer_thickness
sensor_layer_bottoms = [first_layer_bottom, second_layer_bottom, third_layer_bottom, mold_top]

def print_pneunet():

    # The order of these commands is essential to keeping correct alignment and 
    # connections between components. Start with initiating alignment and setting
    # print heights.
    emb3DMatrixPrinting.set_default_travel_height(mold_top, 15)
    ClosedLoopActuator_ActuatorOnly.set_print_heights(second_layer_bottom)
    ClosedLoopActuatorSensors.set_print_heights(sensor_layer_bottoms)              
    CorrectedMultiMaterial.set_cur_tool() # start with A 
    CorrectedMultiMaterial.offset_tools() # align all tips
    
    # The printing should start with the print nozzle on the centerline of the
    # mold and 15 mm to the right of the mold's left edge. Set this (X,Y) 
    # position as (0,0) with POSOFFSET X Y and swap to Material B:
    emb3DPGlobals.g.abs_move(x = start_pos[0], y = start_pos[1])
    CorrectedMultiMaterial.new_change_tool(1) # switch to B
    ClosedLoopActuatorSensors.print_curvature_sensor()
    
    # At this point, the curvature sensor should be done, and the tip out of the
    # mold. Call a long dwell; hit pause on the CNC Operator Software, and prepare
    # the next layer of the mold.
    emb3DPGlobals.g.dwell(30)
    
    # Coming into the new matrix, print the inlets for the curvature sensor:
    ClosedLoopActuatorSensors.print_curvature_sensor_inlet()
    
    # Now ,move back to the temporary (X=0, Y=0) position and begin printing the
    # actuator in the new matrix material; start with the actuator spacers.
    CorrectedMultiMaterial.new_change_tool(0) # switch to A
    emb3DPGlobals.g.abs_move(x = start_pos[0], y = start_pos[1])
    ClosedLoopActuator_ActuatorOnly.print_bladder_spacers() # use A to print spacers
    
    # Now start printing the proprioceptive sensor:
    CorrectedMultiMaterial.new_change_tool(1) # switch to B
    ClosedLoopActuatorSensors.print_connectors() # use B to print connectors
    
    # Print the bladders of the actuator:
    CorrectedMultiMaterial.new_change_tool(0) # change to A
    ClosedLoopActuator_ActuatorOnly.print_bladders() #use C to print bladders
    
    # Finish printing the proprioceptive sensor:
    CorrectedMultiMaterial.new_change_tool(1) #change back to B
    ClosedLoopActuatorSensors.print_better_spokes()  #use B for spokes
    ClosedLoopActuatorSensors.print_fancy_sensor_inlet() #use B for fancy sensor inlet
    ClosedLoopActuatorSensors.print_tops() #use B for tops
    
    # Print the busline and inlet for the actuator:
    CorrectedMultiMaterial.new_change_tool(0) #change to A
    ClosedLoopActuator_ActuatorOnly.print_bladder_bus_line() #use C for bladder bus line
    ClosedLoopActuator_ActuatorOnly.print_bus_line_inlet() #use C for bladder bus line inlet
    
    # At this point, the curvature sensor, prioceptive sensor, and actuator
    # should be done. The tip should be out of the mold. Call a long dwell; hit 
    # pause on the CNC Operator Software, and prepare the next layer of the mold.
    emb3DPGlobals.g.abs_move(x = start_pos[0], y = start_pos[1])
    emb3DPGlobals.g.dwell(30)
    
    # Print the contact sensor:
    CorrectedMultiMaterial.new_change_tool(1) #change to B
    ClosedLoopActuatorSensors.print_contact_sensor_inlet() #use B for sensor inlet
    CorrectedMultiMaterial.new_change_tool(0) #change to A
    emb3DPGlobals.g.abs_move(x = start_pos[0], y = start_pos[1])
    CorrectedMultiMaterial.new_change_tool(1) #change back to B
    
    ClosedLoopActuatorSensors.print_contact_sensor() #use B for sensor
    CorrectedMultiMaterial.new_change_tool(0) #end with A    
    emb3DPGlobals.g.abs_move(x = start_pos[0], y = start_pos[1])
    # Return to the temporary (X=0, Y=0) position and remove all position and 
    # tool offsets:
    CorrectedMultiMaterial.remove_tool_offset()
    
print_pneunet()

emb3DPGlobals.g.view('matplotlib')
emb3DPGlobals.g.teardown()

print "\nALSO, FIX THE PROPRIOCEPTION SENSOR'S AND ALL SENSORS' PARAMETERS; we want to print at 3 mm/s"
print "\nLASTLY, WE NEED TO GO THROUGH AND FIX DWELLS and GRADIENTS OF SPEED IN INLETS"
    