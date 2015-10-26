# -*- coding: utf-8 -*-

"""

ClosedLoopActuatorSensors.py

Ryan Truby, Harvard Lewis Research Group

2015.09.27

Library of mecode functions for printing soft robot pneunet actuators with three
independent sensors: a curvature, proprioceptive, and contact sensor.

Printing notes:
    The bladders, bus line, and spacers are all printed with 25 wt% Pluronic 
    F127 using a 1.5" straight red tip at 88 psi. This summer, we printed the 
    actuators at 85 psi, but I saw poor connectivity at this pressure starting 
    on 2015.09.05.
    
    The matrix is formulated with 10:1 SortaClear 18 with 0.15% Thivex.
    
    All sensing components printed with 25 wt% F127 lavendar tip at 75 psi in 
    Closed Loop Actuator Matrix.

"""

import emb3DMatrixPrinting 
import emb3DPGlobals
import ClosedLoopActuator_ActuatorOnly 

################################################################################
################################################################################

### POWERFUL PARAMETERS THAT AFFECT DIMENSIONS OF SENSORS - from ClosedLoopActuator_ActuatorOnly
num_bladders = ClosedLoopActuator_ActuatorOnly.num_bladders
num_layers = ClosedLoopActuator_ActuatorOnly.num_layers

### SENSOR PRINTING PARAMETERS - For printing with a glass, 30 um tip, 50 psi:
glass_tip_speed_factor = 1                       # = 1 for no glass tip, 0.2 was REALLY slow when printing with 30 wt% F127 at 95 psi.
high_F127_conc_inlet_speed_factor = 0.25
sensor_print_speed = glass_tip_speed_factor * 6  # 5 changed on 8/10/15
sensor_width = 5
sensor_width = 4.0 # added 2015.10.12
sensor_height_offset = 0.5
sensor_length_offset = 3

####### CURVATURE SENSOR PARAMETERS ######
curvature_sensor_width = 4.0
#curvature_sensor_width =  # added 2015.10.11
curvature_sensor_length_offset = 3
curvature_sensor_print_speed = 3

####### FANCY SENSOR PARAMETERS ########
# CONNECTOR PARAMETERS (connectors go below bladders)
connector_height_offset = 1.3 # distance below the bladder print height 
connector_offset= (ClosedLoopActuator_ActuatorOnly.spacer_spacing/2 - ClosedLoopActuator_ActuatorOnly.spacer_width)/2 #halfway between spacers in x-direction
connector_print_speed = glass_tip_speed_factor*2 #1.5 # Pressure: 75 psi changed on 8/10/15
# TOP PARAMETERS (tops go above spacers)
top_height_offset = 1.7 + 1 #how far above spacers, 0.7 added on 20151005, changed to 1 on another print on 20151005
top_y_offset = 0.375*ClosedLoopActuator_ActuatorOnly.spacer_length # distance in from the edges of the spacers (currently halfway) in the y-direction

spoke_print_speed = 2*glass_tip_speed_factor
top_print_speed = 2*glass_tip_speed_factor #1.5 changed on 8/10/15
spoke_print_speed = top_print_speed #spokes connect connectors and tops 

#### INLET PARAMETERS #####
fancy_sensor_inlet_print_speed = 0.5*glass_tip_speed_factor
inlet_length_fancy_sensor = 6.5
inlet_length_bus_line = 6.5
bus_line_inlet_print_speed = 0.5
sensor_inlet_print_speed = 0.5*glass_tip_speed_factor*high_F127_conc_inlet_speed_factor
sensor_inlet_connector_print_speed = 2 * sensor_inlet_print_speed
inlet_length_sensor = 6.5

# Start with substrate_zero at 1 so it will throw a fault on the printer unless
# they are set.
substrate_zero = ClosedLoopActuator_ActuatorOnly.substrate_zero
curvature_layer_bottom = 1
spacer_print_height = substrate_zero + ClosedLoopActuator_ActuatorOnly.spacer_layer_increment
connector_print_height = ClosedLoopActuator_ActuatorOnly.bladder_print_height - connector_height_offset 
top_print_height = spacer_print_height + (ClosedLoopActuator_ActuatorOnly.spacer_layers -1 ) * ClosedLoopActuator_ActuatorOnly.spacer_layer_increment + top_height_offset
fancy_sensor_inlet_print_height = top_print_height - 2 
contact_layer_bottom = 1

################################################################################
################################################################################

# FUNCTION FOR SETTING ALL RELEVANT PRINT HEIGHTS FOR SENSOR COMPONENTS:
def set_print_heights(mold_layer_bottoms):
    # mold_layer_bottoms should have three elements only
    global curvature_layer_bottom                  # for curvature sensor 
    global spacer_print_height                     # for proprioceptive sensor
    global connector_print_height                  # for proprioceptive sensor
    global top_print_height                        # for proprioceptive sensor
    global fancy_sensor_inlet_print_height         # for proprioceptive sensor
    global contact_layer_bottom                    # for contact sensor
    
    curvature_sensor_print_height_offset = (mold_layer_bottoms[0] + mold_layer_bottoms[1])/2
    contact_sensor_print_height_offset = (mold_layer_bottoms[3] + mold_layer_bottoms[2])/2
    
    curvature_layer_bottom = curvature_sensor_print_height_offset
    spacer_print_height = mold_layer_bottoms[1]
    connector_print_height = ClosedLoopActuator_ActuatorOnly.bladder_print_height - connector_height_offset
    top_print_height = spacer_print_height + (ClosedLoopActuator_ActuatorOnly.spacer_layers -1 ) * ClosedLoopActuator_ActuatorOnly.spacer_layer_increment + top_height_offset
    fancy_sensor_inlet_print_height = top_print_height - 3
    contact_layer_bottom = contact_sensor_print_height_offset
    
# CURVATURE SENSOR AT TOP OF ACTUATOR
def print_curvature_sensor():
    emb3DMatrixPrinting.move_y(sensor_width/2)
    emb3DMatrixPrinting.move_x(ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)+(curvature_sensor_length_offset+2))
    emb3DMatrixPrinting.print_mode(print_height_abs = curvature_layer_bottom, print_speed = 20)
    emb3DPGlobals.g.feed(curvature_sensor_print_speed)
    for meander in xrange(2):
        emb3DMatrixPrinting.move_x(-1*ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)-(curvature_sensor_length_offset+2))
        emb3DMatrixPrinting.move_y(-1*curvature_sensor_width/5)
        emb3DMatrixPrinting.move_x(ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)+(curvature_sensor_length_offset+2))
        emb3DMatrixPrinting.move_y(-1*curvature_sensor_width/5)
    emb3DMatrixPrinting.move_x(-1*ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)-(curvature_sensor_length_offset+2))
    emb3DMatrixPrinting.move_y(-1*curvature_sensor_width/5)
    emb3DMatrixPrinting.move_x(ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)+(curvature_sensor_length_offset+2))
    emb3DMatrixPrinting.travel_mode()

# INLET FOR CURVATURE SENSOR
def print_curvature_sensor_inlet():
    ## move these variables up to the top of the script:
    pre_inlet_print_speed = 2
    
    emb3DMatrixPrinting.print_mode(print_height_abs = curvature_layer_bottom, print_speed = 20)
    emb3DPGlobals.g.feed(pre_inlet_print_speed)
    emb3DPGlobals.g.move(z = 4)
    emb3DPGlobals.g.feed(sensor_inlet_print_speed)
    emb3DPGlobals.g.move(x = inlet_length_sensor)
    emb3DMatrixPrinting.travel_mode()
    emb3DPGlobals.g.move(x = -1*inlet_length_sensor, y = sensor_width)
    emb3DMatrixPrinting.print_mode(print_height_abs = curvature_layer_bottom, print_speed = 20)
    emb3DPGlobals.g.feed(pre_inlet_print_speed)
    emb3DPGlobals.g.move(z = 4)
    emb3DPGlobals.g.feed(sensor_inlet_print_speed)
    emb3DPGlobals.g.move(x = inlet_length_sensor)
    emb3DMatrixPrinting.travel_mode() 

# COMPONENT OF FANCY SENSOR BELOW BLADDERS
def print_connectors():
    emb3DMatrixPrinting.travel_mode()
    emb3DMatrixPrinting.move_x(-1*ClosedLoopActuator_ActuatorOnly.spacer_spacing*(ClosedLoopActuator_ActuatorOnly.num_spacers-1)-1*ClosedLoopActuator_ActuatorOnly.bladder_spacing/2.0)
    emb3DPGlobals.g.move(x = -connector_offset, y = -ClosedLoopActuator_ActuatorOnly.spacer_length/2 + top_y_offset)
    for connector in range(num_bladders):
        emb3DMatrixPrinting.print_mode(print_height_abs = connector_print_height, print_speed = connector_print_speed)
        emb3DPGlobals.g.move(x = 2* connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width)
        emb3DMatrixPrinting.travel_mode()
        emb3DPGlobals.g.move(x = ClosedLoopActuator_ActuatorOnly.spacer_spacing - 2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width)
    emb3DPGlobals.g.move(x = -ClosedLoopActuator_ActuatorOnly.spacer_spacing + 2* connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width, y = ClosedLoopActuator_ActuatorOnly.spacer_length - 2*top_y_offset)
    for connector in range(num_bladders):
        emb3DMatrixPrinting.print_mode(print_height_abs = connector_print_height, print_speed = top_print_speed)
        emb3DPGlobals.g.move(x = -2* connector_offset + -ClosedLoopActuator_ActuatorOnly.bladder_width)
        emb3DMatrixPrinting.travel_mode()
        emb3DPGlobals.g.move(x = -ClosedLoopActuator_ActuatorOnly.spacer_spacing + 2* connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width)
    emb3DPGlobals.g.move(x = ClosedLoopActuator_ActuatorOnly.spacer_spacing - connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width)   
    emb3DPGlobals.g.move(y = -ClosedLoopActuator_ActuatorOnly.spacer_length/2 + top_y_offset)  

# COMPONENT OF FANCY SENSOR THAT CONNECTS CONNECTORS AND TOPS
def print_spokes():
    emb3DMatrixPrinting.move_x(-ClosedLoopActuator_ActuatorOnly.bladder_spacing + ClosedLoopActuator_ActuatorOnly.bladder_width + connector_offset) 
    emb3DMatrixPrinting.move_y(-ClosedLoopActuator_ActuatorOnly.spacer_length/2 + top_y_offset)      

    #first moving left on lower value y side
    for spokes in range(num_bladders):
        emb3DMatrixPrinting.print_mode(print_height_abs = connector_print_height, print_speed = spoke_print_speed)
        if (spokes != 0):
            emb3DPGlobals.g.move(z = top_print_height - connector_print_height)               
        else: # if first one, print shorter spoke for inlet
            emb3DPGlobals.g.move(z = fancy_sensor_inlet_print_height- connector_print_height)     
        emb3DMatrixPrinting.travel_mode()
        emb3DPGlobals.g.move(x= -2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width)
        emb3DMatrixPrinting.print_mode(print_height_abs = connector_print_height, print_speed = spoke_print_speed)
        emb3DPGlobals.g.move(z = top_print_height- connector_print_height)              
        emb3DMatrixPrinting.travel_mode()
        ### Edited on 2015.10.22 ######
        ## why is the code below different than the previous g.move(x = ...) move? 
        #emb3DPGlobals.g.move(x = -ClosedLoopActuator_ActuatorOnly.spacer_spacing + 2*connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width) 
        emb3DPGlobals.g.move(x= -2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width) 
        ############################### 
   
    emb3DPGlobals.g.move(x = ClosedLoopActuator_ActuatorOnly.spacer_spacing - 2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width)
    emb3DMatrixPrinting.print_mode(print_height_abs = top_print_height, print_speed = spoke_print_speed)
    emb3DPGlobals.g.move(y = ClosedLoopActuator_ActuatorOnly.spacer_length - 2*top_y_offset)
    emb3DMatrixPrinting.travel_mode()
    
    #then moving right on higher value y side
    for spokes in range(num_bladders):
        emb3DMatrixPrinting.print_mode(print_height_abs = connector_print_height, print_speed = spoke_print_speed)
        emb3DPGlobals.g.move(z = top_print_height - connector_print_height)
        #emb3DPGlobals.g.dwell()
        emb3DMatrixPrinting.travel_mode()
        emb3DPGlobals.g.move(x= 2* connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width)
        emb3DMatrixPrinting.print_mode(print_height_abs = connector_print_height, print_speed = spoke_print_speed)
        if (spokes != num_bladders-1):
            emb3DPGlobals.g.move(z = top_print_height - connector_print_height)
        else:# if first one, print shorter spoke for inlet
            emb3DPGlobals.g.move(z = fancy_sensor_inlet_print_height- connector_print_height)    
        emb3DMatrixPrinting.travel_mode()
        emb3DPGlobals.g.move(x = ClosedLoopActuator_ActuatorOnly.spacer_spacing - 2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width)
        
# created on 2015.10.22 to repair errors in print_spokes()        
def print_better_spokes():
    emb3DMatrixPrinting.move_x(-ClosedLoopActuator_ActuatorOnly.bladder_spacing + ClosedLoopActuator_ActuatorOnly.bladder_width + connector_offset) 
    emb3DMatrixPrinting.move_y(-ClosedLoopActuator_ActuatorOnly.spacer_length/2 + top_y_offset)      

    #first moving left on lower value y side
    for spokes in range(num_bladders):
        emb3DMatrixPrinting.print_mode(print_height_abs = connector_print_height, print_speed = spoke_print_speed)
        if (spokes != 0):
            emb3DPGlobals.g.move(z = top_print_height - connector_print_height)               
        else: # if first one, print shorter spoke for inlet
            emb3DPGlobals.g.move(z = fancy_sensor_inlet_print_height- connector_print_height)     
        emb3DMatrixPrinting.travel_mode()
        emb3DPGlobals.g.move(x= -2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width)
        emb3DMatrixPrinting.print_mode(print_height_abs = connector_print_height, print_speed = spoke_print_speed)
        emb3DPGlobals.g.move(z = top_print_height- connector_print_height)              
        emb3DMatrixPrinting.travel_mode()
        ### Edited on 2015.10.22 ######
        ## why is the code below different than the previous g.move(x = ...) move? 
        #emb3DPGlobals.g.move(x = -ClosedLoopActuator_ActuatorOnly.spacer_spacing + 2*connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width) 
        emb3DPGlobals.g.move(x= -2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width) 
        ############################### 
   
    emb3DPGlobals.g.move(x = ClosedLoopActuator_ActuatorOnly.spacer_spacing - 2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width)
    #emb3DMatrixPrinting.print_mode(print_height_abs = top_print_height, print_speed = spoke_print_speed)
    emb3DPGlobals.g.move(y = ClosedLoopActuator_ActuatorOnly.spacer_length - 2*top_y_offset)
    #emb3DMatrixPrinting.travel_mode()
    
    #then moving right on higher value y side
    for spokes in range(num_bladders):
        emb3DMatrixPrinting.print_mode(print_height_abs = connector_print_height, print_speed = spoke_print_speed)
        emb3DPGlobals.g.move(z = top_print_height - connector_print_height)
        emb3DMatrixPrinting.travel_mode()
        if (spokes == 0):
            emb3DMatrixPrinting.print_mode(print_height_abs = top_print_height, print_speed = spoke_print_speed)
            emb3DPGlobals.g.move(y = -(ClosedLoopActuator_ActuatorOnly.spacer_length - 2*top_y_offset))
            emb3DMatrixPrinting.travel_mode()
            emb3DPGlobals.g.move(y = ClosedLoopActuator_ActuatorOnly.spacer_length - 2*top_y_offset)
        emb3DPGlobals.g.move(x= 2* connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width)
        emb3DMatrixPrinting.print_mode(print_height_abs = connector_print_height, print_speed = spoke_print_speed)
        if (spokes != num_bladders-1):
            emb3DPGlobals.g.move(z = top_print_height - connector_print_height)
        else:# if first one, print shorter spoke for inlet
            emb3DPGlobals.g.move(z = fancy_sensor_inlet_print_height- connector_print_height)    
        emb3DMatrixPrinting.travel_mode()
        emb3DPGlobals.g.move(x = ClosedLoopActuator_ActuatorOnly.spacer_spacing - 2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width)
        
        
#INLET COMPONENT OF FANCY SENSOR
def print_fancy_sensor_inlet():     
    emb3DPGlobals.g.move(x = -ClosedLoopActuator_ActuatorOnly.spacer_spacing + 2* connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width)
    emb3DMatrixPrinting.print_mode(print_height_abs = fancy_sensor_inlet_print_height, print_speed = fancy_sensor_inlet_print_speed)
    emb3DPGlobals.g.move(x = inlet_length_fancy_sensor)
    emb3DMatrixPrinting.travel_mode()
    emb3DPGlobals.g.move(x = -inlet_length_fancy_sensor)
    emb3DPGlobals.g.move(y = 2*(-ClosedLoopActuator_ActuatorOnly.spacer_length/2 + top_y_offset))
    emb3DMatrixPrinting.print_mode(print_height_abs = fancy_sensor_inlet_print_height, print_speed = fancy_sensor_inlet_print_speed)
    emb3DPGlobals.g.move(x = inlet_length_fancy_sensor)
    emb3DMatrixPrinting.travel_mode()
    emb3DPGlobals.g.move(x = -inlet_length_fancy_sensor)
    emb3DPGlobals.g.move(y = ClosedLoopActuator_ActuatorOnly.spacer_length/2 - top_y_offset)
    emb3DMatrixPrinting.travel_mode()
    
# COMPONENT OF FANCY SENSOR THAT GOES ABOVE SPACERS
def print_tops():
    emb3DPGlobals.g.move(x= -2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width, y = -ClosedLoopActuator_ActuatorOnly.spacer_length/2 + top_y_offset )
    for top in range(ClosedLoopActuator_ActuatorOnly.num_spacers):
        emb3DMatrixPrinting.print_mode(print_height_abs = top_print_height, print_speed = top_print_speed)
        emb3DPGlobals.g.move(x = -ClosedLoopActuator_ActuatorOnly.spacer_spacing + 2* connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width)
        emb3DMatrixPrinting.travel_mode()
        emb3DPGlobals.g.move(x = -2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width)
    emb3DPGlobals.g.move(x = 2* connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width)
    emb3DPGlobals.g.move(y =  ClosedLoopActuator_ActuatorOnly.spacer_length - 2*top_y_offset)   
    for top in range(ClosedLoopActuator_ActuatorOnly.num_spacers):
        emb3DMatrixPrinting.print_mode(print_height_abs = top_print_height, print_speed = top_print_speed)
        emb3DPGlobals.g.move(x = ClosedLoopActuator_ActuatorOnly.spacer_spacing - 2* connector_offset - ClosedLoopActuator_ActuatorOnly.bladder_width)
        emb3DMatrixPrinting.travel_mode()
        emb3DPGlobals.g.move(x = 2* connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width)
    emb3DPGlobals.g.move(y = -ClosedLoopActuator_ActuatorOnly.spacer_length/2 + top_y_offset)
    emb3DPGlobals.g.move(x = -2* connector_offset)
    emb3DPGlobals.g.move(x = ClosedLoopActuator_ActuatorOnly.spacer_spacing -  connector_offset + ClosedLoopActuator_ActuatorOnly.bladder_width )
    emb3DMatrixPrinting.travel_mode()
     
# INLET FOR CONTACT SENSOR
def print_contact_sensor_inlet():
    ## move these variables up to the top of the script:
    additional_y_offset_for_inlets = 2
    inlet_height_offset = 5 # before 20151005, this was equal to 4
    pre_inlet_print_speed = 2
    ##
    
    emb3DMatrixPrinting.move_x(ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)+(curvature_sensor_length_offset+2) + inlet_length_sensor)
    emb3DMatrixPrinting.move_y(sensor_width/2 + additional_y_offset_for_inlets)    
    emb3DMatrixPrinting.print_mode(print_height_abs = contact_layer_bottom - inlet_height_offset, print_speed = 20)
    emb3DPGlobals.g.feed(sensor_inlet_print_speed)
    emb3DPGlobals.g.move(x = -1 * inlet_length_sensor)
    emb3DPGlobals.g.feed(pre_inlet_print_speed)
    emb3DPGlobals.g.move(z = inlet_height_offset)
    #emb3DPGlobals.g.move(y = -1 * additional_y_offset_for_inlets)
    emb3DMatrixPrinting.travel_mode()
    emb3DPGlobals.g.move(x = inlet_length_sensor, y = -1*sensor_width - 2 * additional_y_offset_for_inlets)
    emb3DMatrixPrinting.print_mode(print_height_abs = contact_layer_bottom - inlet_height_offset, print_speed = 20)
    emb3DPGlobals.g.feed(sensor_inlet_print_speed)
    emb3DPGlobals.g.move(x = -1 * inlet_length_sensor)
    #emb3DPGlobabls.g.move(y = additional_y_offset_for_inlets)
    emb3DPGlobals.g.feed(pre_inlet_print_speed)
    emb3DPGlobals.g.move(z = inlet_height_offset)
    emb3DMatrixPrinting.travel_mode()

# CONTACT SENSOR AT TOP OF ACTUATOR
def print_contact_sensor():
    ## move these variables up to the top of the script:
    additional_y_offset_for_inlets = 2
    inlet_height_offset = 5 # before 20151005, this was equal to 4
    ##
    
    emb3DMatrixPrinting.move_x(ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)+(curvature_sensor_length_offset+2))
    emb3DMatrixPrinting.move_y(sensor_width/2 + additional_y_offset_for_inlets)
    emb3DMatrixPrinting.print_mode(print_height_abs = contact_layer_bottom, print_speed = 20)
    emb3DPGlobals.g.feed(curvature_sensor_print_speed)
    emb3DMatrixPrinting.move_y(-1*additional_y_offset_for_inlets)
    for meander in xrange(2):
        emb3DMatrixPrinting.move_x(-1*ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)-(curvature_sensor_length_offset+2))
        emb3DMatrixPrinting.move_y(-1*curvature_sensor_width/5)
        emb3DMatrixPrinting.move_x(ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)+(curvature_sensor_length_offset+2))
        emb3DMatrixPrinting.move_y(-1*curvature_sensor_width/5)
    emb3DMatrixPrinting.move_x(-1*ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)-(curvature_sensor_length_offset+2))
    emb3DMatrixPrinting.move_y(-1*curvature_sensor_width/5)
    emb3DMatrixPrinting.move_x(ClosedLoopActuator_ActuatorOnly.bladder_spacing*(num_bladders-0.5)+(curvature_sensor_length_offset+2))
    emb3DMatrixPrinting.move_y(-1*additional_y_offset_for_inlets)
    emb3DMatrixPrinting.travel_mode()


    
    

