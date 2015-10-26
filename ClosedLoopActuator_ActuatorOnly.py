# -*- coding: utf-8 -*-

"""

ClosedLoopActuator_ActuatorOnly.py

Ryan Truby, Harvard Lewis Research Group

2015.09.27

Library of mecode functions for printing soft robot pneunet actuators with three
independent sensors: a curvature, proprioceptive, and contact sensor.

Printing notes:
    The bladders, bus line, and spacers are all printed with 25 wt% Pluronic 
    F127 using a 1.5" straight red tip at 88 psi
    
    The matrix is formulated with 10:1 SortaClear 18 with 0.15% Thivex.

"""

import emb3DMatrixPrinting 
import emb3DPGlobals

################################################################################
################################################################################
    
# POWERFUL PARAMETERS THAT AFFECT DIMENSIONS
num_bladders = 6                       # should be 6
num_layers = 12 - 2                    # We had always printed 12 layers; for the three-layer mold, this needs to be 11; 11 was too much for the 12.7 mm thick actuator layer
    
# SPACER PARAMETERS
spacer_print_speed = 2.0               # Pressure: 88 psi
spacer_layers = int(num_layers)        # num_layers designated at execution line
spacer_layer_increment = 0.8 
spacer_spacing = 9.0                   # float value required
spacer_length = 14.0                   # float value required
spacer_width = 0.8
num_spacers = num_bladders - 1         # bladders at both ends
edge_reduction_factor = 0.3            # reducing this further from 0.5 on 2015.09.30 to really force pluronic touching mold edge

# BLADDER PARAMETERS
bladder_print_speed = 2.0              # Pressure: 88 psi
bladder_layers = int(num_layers)       # num_layers designated at execution line
bladder_layer_increment = 0.8 
bladder_spacing = spacer_spacing
bladder_length = spacer_length - 3
bladder_width = 0.8 

# BUS LINE PARAMETERS
bus_line_print_speed = 1.0
bus_line_print_speed = 3.0 # added on 2015.10.11
bus_line_inlet_print_speed = 0.5
bus_line_length = num_spacers * spacer_spacing
inlet_length_bus_line = 6.5

# Start with substrate_zero at 1 so it will throw a fault on the printer unless
# they are set.
substrate_zero = 1
spacer_print_height = substrate_zero + spacer_layer_increment
bladder_print_height = (3 * spacer_layer_increment) + substrate_zero
bus_line_print_height = bladder_print_height + ((bladder_layers+1) * bladder_layer_increment)
bus_line_print_height = bladder_print_height + bladder_layers*bladder_layer_increment # added on 2015.10.11

################################################################################
################################################################################

# FUNCTION FOR SETTING ALL RELEVANT PRINT HEIGHTS FOR ACTUATOR COMPONENTS:
def set_print_heights(mold_layer_bottom):
    global substrate_zero
    global spacer_print_height
    global bladder_print_height
    global bus_line_print_height
    
    substrate_zero = mold_layer_bottom
    spacer_print_height = substrate_zero + spacer_layer_increment
    bladder_print_height = (3 * spacer_layer_increment) + substrate_zero
    bladder_print_height = (3.5 * spacer_layer_increment) + substrate_zero # added on 2015.10.26
    bus_line_print_height = bladder_print_height + ((bladder_layers + 1) * bladder_layer_increment) 
    bus_line_print_height = bladder_print_height + bladder_layers*bladder_layer_increment # added on 2015.10.11
    
    # We're running into similar issues as I saw with optimizing the printing of octobot's actuators:
    # we need to overpump the spacer ink to ensure that no actuator matrix gets between the spacers
    # and the curvature sensor. By having the spacer_print_height equal to 
    #     spacer_print_height = substrate_zero + spacer_layer_increment
    # where substrate_zero is the true zero of the curvature sensor matrix, I nearly got
    # complete removal of the actuator matrix between the spacer and the curvature sensor. Set the 
    # following variable to try honing in with a perfect interface between the curvature sensor
    # and the spacer:
    
    spacer_offset = 0.5
    
    spacer_print_height = spacer_print_height - spacer_offset # added on 2015.10.11
    bladder_print_height = bladder_print_height - spacer_offset # added on 2015.10.11
    bus_line_print_height = bus_line_print_height - spacer_offset # added on 2015.10.11
    
    print "The difference between the bus_line_print_height and the mold bottom is " + str(substrate_zero - bus_line_print_height)  
    print bladder_print_height 
    

# HELPER FUNCTION: USED FOR PRINTING VOID LAYERS OF BLADDERS
def print_void_layer(length, width):
    emb3DMatrixPrinting.move_y(length/2.0)
    emb3DMatrixPrinting.move_x(width)
    emb3DMatrixPrinting.move_y(-1*length)
    emb3DMatrixPrinting.move_x(-1*width)
    emb3DMatrixPrinting.move_y(length/2.0)
    
    
# HELPER FUNCTION: USED FOR PRINTING VOID LAYERS OF SPACERS with changing speeds on edges
def print_spacer_void_layer(length, width):
    emb3DPGlobals.g.feed(spacer_print_speed)
    emb3DMatrixPrinting.move_y(length/2.0)
    emb3DPGlobals.g.feed(spacer_print_speed * edge_reduction_factor)
    emb3DMatrixPrinting.move_x(width)
    emb3DPGlobals.g.feed(spacer_print_speed)
    emb3DMatrixPrinting.move_y(-1*length)
    emb3DPGlobals.g.feed(spacer_print_speed * edge_reduction_factor)
    emb3DMatrixPrinting.move_x(-1*width)
    emb3DPGlobals.g.feed(spacer_print_speed)
    emb3DMatrixPrinting.move_y(length/2.0)

# VOID COMPONENT THAT ALLOWS RAPID, HIGH-DISPLACEMENT ACTUATION
def print_bladder_spacers():
    emb3DMatrixPrinting.travel_mode()
    for spacer in range(num_spacers):
        emb3DMatrixPrinting.move_x(spacer_spacing)
        ######### 2015.10.12  spacer_print_height = substrate_zero + spacer_layer_increment
        emb3DMatrixPrinting.print_mode(print_height_abs = spacer_print_height, print_speed = 20)
        emb3DPGlobals.g.feed(spacer_print_speed)
        for layer in range(spacer_layers):
            print_spacer_void_layer(length = spacer_length, width = spacer_width)
            emb3DPGlobals.g.feed(10)
            emb3DPGlobals.g.move(z = spacer_layer_increment)
            emb3DPGlobals.g.feed(spacer_print_speed)
        emb3DMatrixPrinting.travel_mode()

# COMPONENT OF ACTUATOR THAT IS PRESSURIZED
def print_bladders():
    for bladder in range(num_bladders):    
        emb3DMatrixPrinting.print_mode(print_height_abs = bladder_print_height, print_speed = 20)
        emb3DPGlobals.g.feed(bladder_print_speed)
        for layer in range(bladder_layers):
            print_void_layer(length = bladder_length, width = bladder_width)
            emb3DPGlobals.g.move(z = bladder_layer_increment)
        emb3DMatrixPrinting.travel_mode()
        emb3DMatrixPrinting.move_x(bladder_spacing)
            
# LINE THAT CONNECTS ALL THE BLADDERS   
def print_bladder_bus_line():
    emb3DMatrixPrinting.move_x(-1*bladder_spacing*(num_bladders) + 0.25*bladder_spacing)        # the 0.25*bladder_spacing offset gets the bus bar right over the last bladder and prevents crosstalk with fancy sensor
    emb3DMatrixPrinting.print_mode(print_height_abs = bus_line_print_height, print_speed = bus_line_print_speed)          
    emb3DMatrixPrinting.move_x(bladder_spacing*(num_bladders-0.5))       ### the -0.5 could be a variable

# INLET FOR THE BUS LINE   
def print_bus_line_inlet():
    emb3DPGlobals.g.feed(bus_line_inlet_print_speed)
    emb3DMatrixPrinting.move_x(inlet_length_bus_line)
    emb3DMatrixPrinting.travel_mode()
    emb3DMatrixPrinting.move_x(-inlet_length_bus_line)

    
