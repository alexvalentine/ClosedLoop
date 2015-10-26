# -*- coding: utf-8 -*-

"""



Filename: MultiMaterial.py

Author: Ryan L. Truby

Affiliation: Lewis Research Group, Harvard University

Data: 2015.01.19



Description:

    This library contains mecode functions for handling multiple printheads. 

    This code is an adaptation of Dan Fitzgerald's script "MultiMaterial.py". 

    

"""



# Line underneath commented out by RTruby on 2014.09.10 during Experiment C-95

#from aerotech_automation import AerotechAutomator

# Lines underneath added by RTruby on 2014.09.10 during Experiment C-95 during Experiment C-95


from mecode import G

from aerotech_automator import AerotechAutomator



import emb3DMatrixPrinting

import emb3DPGlobals

import os



cur_filepath = os.path.dirname(os.path.realpath(__file__))

print "FILE PATH IS " + str(cur_filepath)+"."

splitted = cur_filepath.split('/')

n=len(splitted)

cur_dir = ''.join((dir+'/') for dir in splitted[:n-1])

#------------------------------------------------------------------------------

# RTruby, 2014.09.10 - Code below commented out during Experiment C-95:

#

#importFileDir = cur_dir+"mecode\\automation_values.json"

#

# Code below added when previous code was commented out:

print cur_dir+"automation_values_ADV.json" 

importFileDir = r"C:\Users\Lewis Group\Documents\GitHub\ClosedLoop\automation_values_ADV.json"

#------------------------------------------------------------------------------

print "Importing nozzle offsets from file " + str(importFileDir)



automator = AerotechAutomator()

automator.load_state(importFileDir)



#Ax_groove, Ay_groove, zA_granite = automator.home_positions['A']

#Bx_groove, By_groove, zB_granite = automator.home_positions['B']

#Cx_groove, Cy_groove, zC_granite = automator.home_positions['C']

#

#

#x_grooves = [Ax_groove, Bx_groove, Cx_groove]

#y_grooves = [Ay_groove, By_groove, Cy_groove]

#z_granites = [zA_granite, zB_granite, zC_granite]

#

#

#print "Nozzle A home at (" + str(Ax_groove) + ", " + str(Ay_groove) + ", " + str(zA_granite) + ")"

#print "Nozzle B home at (" + str(Bx_groove) + ", " + str(By_groove) + ", " + str(zB_granite) + ")"

#print "Nozzle C home at (" + str(Cx_groove) + ", " + str(Cy_groove) + ", " + str(zC_granite) + ")"



# for printing on RoboMama:

tool_axis = (["A","B","C","D"] )#if e3Demb3DPGlobals.Aerotech else ["z","z","z","z"])

line_pressures = [85,33,87,88]

com_ports = [1, 4, 1, 9] 



cur_tool_index = 0

cur_tool = tool_axis[cur_tool_index]

print "MultiMaterial.py thinks this is the current tool: "

print cur_tool

cur_pressure=line_pressures[cur_tool_index]

cur_com_port = com_ports[cur_tool_index]



# for printing on Megacaster:

#tool_axis = (["Z"])

#com_ports = [16]

#cur_tool_index = 0

#cur_tool = tool_axis[cur_tool_index]

#print "MultiMaterial.py thinks this is the curret tool "

#print cur_tool

#cur_com_port = com_ports[cur_tool_index]



def set_cur_tool():

    """"Helper funciton. Sets the current axis letter, pressure, and com port to those corresponding the the current tool index."""

    

    global cur_tool

    global cur_pressure

    global cur_com_port

    

    emb3DMatrixPrinting.turn_pressure_off()

    cur_tool = tool_axis[cur_tool_index]

#    cur_pressure=line_pressures[cur_tool_index]

    cur_com_port = com_ports[cur_tool_index]

    
    

    

#    emb3DPGlobals.g.set_pressure(cur_com_port, cur_pressure)



def offset_tools():

    first_tool = cur_tool

    

    #print "HERE"

    #print automator.home_positions

    #for tool in automator.home_positions:

    #    print automator.home_positions[tool]

    

    emb3DPGlobals.g.write("; LOOK HERE FOR NOZZLE Z OFFSETTING")

    

    height_to_zero_to = emb3DMatrixPrinting.default_mold_z_zero

    

    for tool in automator.home_positions:

        emb3DPGlobals.g.write("G90 ; absolute mode")

        #won't there still be pos/neg problems? if first tool is higher than tool

        str_new_nozzle_offset_z = str(automator.home_positions[tool][2] - automator.home_positions[first_tool][2])

        emb3DPGlobals.g.write("G1 " + tool + "" + str(height_to_zero_to))

        emb3DPGlobals.g.write("G91 ; incremental mode")

        emb3DPGlobals.g.write("G1 " + tool + "" + str(str_new_nozzle_offset_z))

        emb3DPGlobals.g.write("G92 " + tool + str(height_to_zero_to))



def remove_tool_offset():

    emb3DPGlobals.g.write("POSOFFSET CLEAR X Y U A B C D")

    emb3DPGlobals.g.write("G53 ; clear any current fixture offset")



def new_change_tool(to_tool_index):

    """Change the current nozzle and default z axis."""

    

    
    

    if (cur_tool_index != to_tool_index):

        

        global cur_tool_index

        global cur_tool

        old_tool = cur_tool 

        cur_tool_index = to_tool_index

        set_cur_tool()

        

        emb3DPGlobals.g.write("\n; Change Tools from " + old_tool + " to " + tool_axis[cur_tool_index] + ".")

        emb3DPGlobals.g.rename_axis(z=cur_tool)

        print "Renaming Z axis to " + cur_tool + "."

        

        str_new_nozzle_offset_x = str(automator.home_positions[cur_tool][0] - automator.home_positions[old_tool][0])

        str_new_nozzle_offset_y = str(automator.home_positions[cur_tool][1] - automator.home_positions[old_tool][1])

        

        emb3DPGlobals.g.write("G1 X" + str_new_nozzle_offset_x + " Y" + str_new_nozzle_offset_y + " ; set a new fixture offset to compensate for the new tools offset.\n")

    

    else:

        print "ERROR: Switched to tool currently in use!"



def change_tool(to_tool_index):

    """Change the current nozzle and default z axis."""

    

    print "LOOK HERE FOR CURRENT TOOL"

    print " "

    print cur_tool_index

    print "And for next tool:"

    print to_tool_index

    

    if (cur_tool_index != to_tool_index):

        

        global cur_tool_index

        global cur_tool

        old_tool = cur_tool

        cur_tool_index = to_tool_index

        set_cur_tool()

        

        emb3DPGlobals.g.write("\n; Change Tools from " + old_tool + " to " + tool_axis[cur_tool_index] + ".")

        

        emb3DPGlobals.g.rename_axis(z=cur_tool)

        print "Renaming Z axis to " + cur_tool + "."

        

        str_new_nozzle_offset_x = str(automator.home_positions[cur_tool][0] - automator.home_positions[old_tool][0])

        str_new_nozzle_offset_y = str(automator.home_positions[cur_tool][1] - automator.home_positions[old_tool][1])

        str_new_nozzle_offset_z = str(automator.home_positions[cur_tool][2] - automator.home_positions[old_tool][2])

        

        print "STR_NEW_NOZZLE_OFFSET_Z"

        print str_new_nozzle_offset_z

        print automator.home_positions[cur_tool]

        

        emb3DPGlobals.g.write("G53 ; clear any current fixture offset")

        emb3DPGlobals.g.write("POSOFFSET CLEAR X Y U A B C D")

        emb3DPGlobals.g.write("G90 ; absolute mode")

        z_offset = emb3DMatrixPrinting.default_mold_z_zero

        emb3DPGlobals.g.write("G1 " + cur_tool + "" + str(z_offset))

        emb3DPGlobals.g.write("G91 ; incremental mode")

        emb3DPGlobals.g.write("G1 X" + str_new_nozzle_offset_x + " Y" + str_new_nozzle_offset_y + " " + cur_tool + str_new_nozzle_offset_z + " ; set a new fixture offset to compensate for the new tools offset.\n")

        emb3DPGlobals.g.write("G92 X0 Y0 " + cur_tool + str(z_offset))

        

        #emb3DPGlobals.g.write("G53 ; clear any current fixture offset\nG1 X" + str_new_nozzle_offset_x + " Y" + str_new_nozzle_offset_y + " " + cur_tool + str_new_nozzle_offset_z + " ; set a new fixture offset to compensate for the new tools offset.\n")

        #emb3DPGlobals.g.write("G92 X0 Y0 " + cur_tool + "0")

        #if (to_tool_index == 0):

        #    emb3DPGlobals.g.write("G53 ; clear current fixture offset to use Nozzle A (default and homes with position offset)\n")

        #else:    

        #    str_new_nozzle_offset_from_A_x = str(x_grooves[cur_tool_index] - Ax_groove) #"($"+cur_tool+"x-$Ax-($"+cur_tool+"x_dif-$Ax_dif))" #"($Ax_diff-$"+cur_tool+"x_diff)"

        #    str_new_nozzle_offset_from_A_y = str(y_grooves[cur_tool_index] - Ay_groove) #"($Ay-$"+cur_tool+"y+($Ay_dif-$"+cur_tool+"y_dif))" #"($Ay_diff-$"+cur_tool+"y_diff)"

        #    str_new_nozzle_offset_from_A_z = str(z_granites[cur_tool_index] - zA_granite) #"($zMeasureA-$zMeasure"+cur_tool+")"  #+($Az_diff-$"+cur_tool+"z_diff))" #"($Az_diff-$"+cur_tool+"z_diff)"

        #

        #    emb3DPGlobals.g.write("G53 ; clear any current fixture offset\nG54 X" + str_new_nozzle_offset_from_A_x + " Y" + str_new_nozzle_offset_from_A_y + " " + cur_tool + str_new_nozzle_offset_from_A_z + " ; set a new fixture offset to compensate for the new tools offset.\n")

        #    #    emb3DPGlobals.g.write("G1 X(($" + cur_tool + "x-$" + from_tool + "x-($" + cur_tool + "x_dif-$" + from_tool + "x_dif))) F" + str(emb3DMatrixPrinting.default_air_travel_speed))

        #    #    emb3DPGlobals.g.write("G1 Y(($" + from_tool + "y-$" + cur_tool + "y+($" + from_tool + "y_dif-$" + cur_tool + "y_dif)))")



    else:

        print "ERROR: Switched to tool currently in use!"

