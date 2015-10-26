# -*- coding: utf-8 -*-

"""
Filename: emb3DMatrixPrinting.py
Author: Ryan L. Truby
Affiliation: Lewis Research Group, Harvard University
Date: 2015.09.27

Description:

    This library contains mecode functions for handling multiple printheads for
    embedded 3D (emb3D) printing. 

"""

# -*- coding: utf-8 -*-

import numpy as np

import emb3DPGlobals
import CorrectedMultiMaterial
import emb3DMatrixPrinting

################################################################################
#
#   DEFAULT PRINTING PARAMETERS - all dimensions are in mm, s, mm/s
#
################################################################################

default_air_travel_speed = 40                # travel speed in air (movement above the mold)
default_matrix_travel_speed = 12.0           # speed to travel while tip is in matrix
default_print_speed = 1.5                    # print speed used for most channels/traces
default_start_stop_dwell_time = 0.5          # ink hysteresis compensation. Dwell for this long after starting extrusion but before moving, and after stopping but before stopping extrusion
#default_inlet_length = 2                    # length of needle insertion inlets
#default_inlet_print_speed = 0.5             # speed for making needle insertion inlets
default_mold_z_zero = -20                    # HAVE TO CHECK THIS, zero at mold top
default_travel_height_offset = 5             # Add this to default_mold_z_zero to have a safe travel height
default_travel_height_abs = default_mold_z_zero + default_travel_height_offset # height above the work zero to travel in air

def set_default_travel_height(calculated_zero, travel_height_offset):
    global default_mold_z_zero 
    global default_travel_height_offset
    global default_travel_height_abs
    
    default_mold_z_zero = calculated_zero
    default_travel_height_offset = travel_height_offset
    default_travel_height_abs = calculated_zero + travel_height_offset
    
    print "New travel height is " 
    print default_travel_height_abs

################################################################################
#
#   Pressure Control
#
################################################################################

pressure_on = False

def turn_pressure_off(com_port = -1, start_stop_dwell_time = default_start_stop_dwell_time):
    """If the current nozzle's (CorrectedMultiMaterial.cur_tool) pressure is not on, turns it on"""
    
    global pressure_on
    if (pressure_on):
        #get around the inability to use global vars as default arg values
        if (com_port == -1):
            com_port=CorrectedMultiMaterial.cur_com_port
        emb3DPGlobals.g.write("; Toggle pressure on com port " + str(com_port) + " to turn tool " + CorrectedMultiMaterial.cur_tool + " off.")
        
        emb3DPGlobals.g.toggle_pressure(com_port)
        emb3DPGlobals.g.dwell(start_stop_dwell_time)
        pressure_on = False

def turn_pressure_on(com_port = -1, start_stop_dwell_time = default_start_stop_dwell_time):
    """If the current nozzle's (CorrectedMultiMaterial.cur_tool) pressure is on, turns it off"""
        
    global pressure_on
    if (not pressure_on):
        #get around the inability to use global vars as default arg values
        if (com_port == -1):
            com_port=CorrectedMultiMaterial.cur_com_port
        emb3DPGlobals.g.write("; Toggle pressure on com port " + str(com_port) + " to turn tool " + CorrectedMultiMaterial.cur_tool + " on.")
        
        emb3DPGlobals.g.dwell(start_stop_dwell_time)
        emb3DPGlobals.g.toggle_pressure(com_port)
        pressure_on = True


###############################################################################
#
#   Printing and Travel Modes
#
################################################################################

def travel_mode(travel_speed = default_air_travel_speed):
    """"Stop Extrusion, move to travel height"""
    
    emb3DPGlobals.g.write("\n; Enter Travel Mode to height " + str(default_travel_height_abs) + " where mold top is " + str(default_mold_z_zero)) 
   
    last_pos = (emb3DPGlobals.g.position_history[-1] if len(emb3DPGlobals.g.position_history)>0 else None)
    last_z = (last_pos[2] if (last_pos is not None) else -np.inf)
#    print "TRAVEL_MODE: last_pos was " + str(last_pos) + " last_z was " + str(last_z)
    turn_pressure_off()
    if (last_z < default_mold_z_zero):
        move_z_abs(default_mold_z_zero, vertical_travel_speed=emb3DMatrixPrinting.default_matrix_travel_speed)
    move_z_abs(default_travel_height_abs, vertical_travel_speed = travel_speed)  
    
    #    print "Travel mode to height " + str((last_pos[2] if (last_pos) else np.inf))
    emb3DPGlobals.g.write("; Now in travel mode.") 
    
def print_mode(print_height_abs, travel_speed = default_matrix_travel_speed, print_speed = default_print_speed):
    """Move to print height, start Extrusion"""
    
    emb3DPGlobals.g.write("\n; Enter Print Mode to print height " + str(print_height_abs) + " where mold top is " + str(default_mold_z_zero)) 
    
    # go down to to mold zero if we're above it
    last_pos = (emb3DPGlobals.g.position_history[-1] if len(emb3DPGlobals.g.position_history)>0 else None)
    last_z = (last_pos[2] if (last_pos is not None) else -np.inf)
#    print "PRINT_MODE: last_pos was " + str(last_pos) + " last_z was " + str(last_z)
    if (last_z > default_mold_z_zero):
        move_z_abs(default_mold_z_zero, vertical_travel_speed=default_air_travel_speed)
        
    # go the rest of the way in the default_matrix_travel_speed
    if (print_height_abs<default_mold_z_zero):
        move_z_abs(print_height_abs,  vertical_travel_speed=travel_speed)
    else:
        print "e3DMatrixPrinting - print_mode() ERROR: printmode print_height_abs " + str(print_height_abs) + " is above the mold_z_zero " + str(default_mold_z_zero) + "!"
    turn_pressure_on()
    emb3DPGlobals.g.feed(print_speed)
    emb3DPGlobals.g.write("; Now in print mode.") 
    

###############################################################################
#
#   Movement
#
################################################################################

def move_z_abs(height, vertical_travel_speed = default_matrix_travel_speed): #z_axis = "DEFAULT",
    """Move the given z axis in absolute work coordinates"""
            
    #TODO: end on the same print speed we began on
    #maybe move slower while under mold_z_abs
    last_pos = (emb3DPGlobals.g.position_history[-1] if len(emb3DPGlobals.g.position_history)>0 else None)
    last_z = (last_pos[2] if (last_pos is not None) else -np.inf)
    #print "move_abs_z: Last Pos is " + str(last_pos) + " last z is " + str(last_z) + "."

    if (height-last_z != 0):
        emb3DPGlobals.g.feed(vertical_travel_speed)
        emb3DPGlobals.g.abs_move(z=height)
        last_z=height
    else:
        print "WARNING: abs z move of 0 length!"
    
def move_x(distance, theta=0):
    global g
    if (distance==0):
        print "e3DMatrixPrinting - move_y WARNING:No y movement!"
    emb3DPGlobals.g.move(x=np.cos(theta)*distance, y=np.sin(theta)*distance)        
     
def move_y(distance, theta=0):
    global g
    if (distance==0):
        print "e3DMatrixPrinting - move_x WARNING:No x movement!"
    emb3DPGlobals.g.move(x=-np.sin(theta)*distance, y=np.cos(theta)*distance)                     
 
def move_xy(x_distance, y_distance, theta=0):
    global g
    C=np.cos(theta)
    S=np.sin(theta)
    if (x_distance==0 and y_distance==0):
        print "e3DMatrixPrinting - move_xy WARNING:No x or y movement!"
    emb3DPGlobals.g.move(x=x_distance*C-y_distance*S, y=x_distance*S+y_distance*C)