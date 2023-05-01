import pydicom as pd
import numpy as np
import os
import sys
from datetime import datetime

"""
    This script takes a template dicom plan and generates a new set of beam positiions
    the beam positions have the same energy and are evenlyspaced with equal MU

    TODO have field number as an input that clones the current field a specified number of times
"""

"""
    For Mik:
    import pydicom as pd
    dcm = pd.dcmread(plan_file)
    spot_positions = dcm[0x300a,0x03a2][0][0x300a,0x3a8][0][0x300a,0x0394].value
"""

#UCLH spot sizes from plans created at these energies
spot_sizes = {

                '150' : [9.02957534790039, 9.31826114654541],
                '160' : [8.779058456420898, 9.119752883911133],
                '170' : [8.603846549987793, 8.9423189163208],
                '180' : [8.472640991210938, 8.749543190002441],
                '190' : [8.417781829833984, 8.459492683410645],
                '200' : [8.279143333435059, 8.120920181274414]

}
#readin DICOM file that acts as template
dcm = pd.dcmread(sys.argv[1])
offset_spot = 0
pattern_scan = 0
if int(sys.argv[2]) == 1:
    offset_spot = 1 # offset spot should be 0 or 1 depending on if an outside spot is needed for triggeringsys
    print("yeah")
elif int(sys.argv[2]) == 2:
    pattern_scan = 1

beam_sequence = dcm[0x300a,0x03a2].value
#find reference sequence to set total MU
reference_beam_sequence = dcm[0x300a,0x0070][0][0x300c,0x004].value
#dose per mu of this plan - calculated based on a briveous plan with a uniform field
#number of beams
N_beams=len(beam_sequence)
#number of spots per beam
dose_list = []
mu_list = []
energy_list = []
mu_per_spot_list = []
x_field_list = []
y_field_list = []
N_spots_list = []
mu_per_offset_spot_list = []
field_offset_x_list = []
field_offset_y_list = []
spacing_list = []

for i in range(1,N_beams+1):
    #get paramters for editing
    print(f"Set energy for beam {i}")
    energy_to_set = int(input())
    energy_list.append(energy_to_set)

for i in range(1,N_beams+1):
    print(f"Set X field size for beam {i}")
    x_field = float(input())
    x_field_list.append(x_field*10)
    print(f"Set Y field size for beam {i}")
    y_field = float(input())
    y_field_list.append(y_field*10)

for i in range(1,N_beams+1):
    print(f"Set X field offset for beam {i}")
    x_field_offset = float(input())
    field_offset_x_list.append(x_field_offset*10)
    print(f"Set Y field offset for beam {i}")
    y_field_offset = float(input())
    field_offset_y_list.append(y_field_offset*10)
for i in range(1,N_beams+1):
    print(f"Set beam spacing for beam {i}")
    spacing = float(input())
    spacing_list.append(spacing)

i=0
for beam in beam_sequence:
    spot_list = []
    spot_size = spot_sizes[str(energy_list[i])]
    beam[0x300a,0x03a8][0][0x300a,0x0398].value = spot_size
    beam[0x300a,0x03a8][1][0x300a,0x0398].value = spot_size
    spot_spacing_x = spacing_list[i]#spot_size[0]/1.5
    spot_spacing_y = spacing_list[i]#spot_size[1]/1.5
    pos_x = np.arange((-x_field_list[i]/2)+(spot_spacing_x/2)+field_offset_x_list[i],(x_field_list[i]/2)+field_offset_x_list[i], spot_spacing_x)
    pos_y = np.arange((-y_field_list[i]/2)+(spot_spacing_y/2)+field_offset_y_list[i],(y_field_list[i]/2)+field_offset_y_list[i], spot_spacing_y)
    if pattern_scan:
        for it in range(0,len(pos_x)):
            print(it)
            for x in range(0,len(pos_x)):
                for position in range(0,int(y_field_list[i]),50):
                    for y in range(0,len(pos_y)):
                        if y == position:
                            spot_list.append(pos_x[x-it])
                            spot_list.append(pos_y[y-it])
    else:
        for position_x in pos_x:
            for position_y in pos_y:
                spot_list.append(position_x)
                spot_list.append(position_y)
                if offset_spot:
                    spot_list.append(0.0)
                    spot_list.append(150.0)

    #print(spot_list)

    N_spots_list.append(int(len(spot_list)/2))
    beam[0x300a,0x03a8][0][0x300a,0x0392].value = N_spots_list[i]
    beam[0x300a,0x03a8][0][0x300a,0x0394].value = spot_list

    beam[0x300a,0x03a8][1][0x300a,0x0392].value =N_spots_list[i]
    beam[0x300a,0x03a8][1][0x300a,0x0394].value = spot_list
    i+=1
    print(f'Beam Number: {i+1}, Number of spots: {len(spot_list)/2}')

for i in range(1,N_beams+1):
    #get paramters for editing
    print(f"Set MU for beam {i}")
    MU_per_spot = int(input())
    mu_per_spot_list.append(MU_per_spot)
    MU_to_set = int((N_spots_list[i-1] * MU_per_spot)/4)
    mu_list.append(MU_to_set)
    #divided by 30 as initial plan had 30 MU
if offset_spot:
    for i in range(1,N_beams+1):
        print(f"Set MU for offset spots {i}")
        MU_offset_spot = int(input())
        mu_per_offset_spot_list.append(MU_offset_spot)
        MU_additional = int((N_spots_list[i-1] * MU_offset_spot)/4)
        mu_list[i-1] = mu_list[i-1] + MU_additional
        beam_dose_MU = (0.39874674121094)/(30*289)
        in_beam_dose = 0.5*beam_dose_MU*mu_per_spot_list[i-1]*N_spots_list[i-1]
        offset_dose = 0.5*beam_dose_MU*MU_additional*N_spots_list[i-1]
        dose_list.append(in_beam_dose+offset_dose)
else:
    for i in range(1,N_beams+1):
        MU_offset_spot = 0
        mu_per_offset_spot_list.append(MU_offset_spot)
        MU_additional = int((N_spots_list[i-1] * MU_offset_spot)/4)
        mu_list[i-1] = mu_list[i-1] + MU_additional
        beam_dose_MU = (0.39874674121094)/(30*289)
        in_beam_dose = 0.5*beam_dose_MU*mu_per_spot_list[i-1]*N_spots_list[i-1]
        offset_dose = 0.5*beam_dose_MU*MU_additional*N_spots_list[i-1]
        dose_list.append(in_beam_dose+offset_dose)

print("Enter gantry number: ")
gantry_number = input()

#print("MU list: ", mu_list)
#print("Energy list: ", energy_list)
#print("Dose list: ", dose_list)




#set required parameters
i = 0
for beam in beam_sequence:
    beam[0x300a, 0x00b2].value = f"Gantry {gantry_number}"
    beam[0x300a,0x010e].value = mu_list[i]
    beam[0x300a,0x03a8][0][0x300a,0x0114].value = energy_list[i]
    beam[0x300a,0x03a8][-1][0x300a,0x0134].value = mu_list[i]
    beam[0x300a,0x03a8][0][0x300a,0x0396].value = N_spots_list[i]*[int(mu_per_spot_list[i]/2)]

    for spot_number in range(0,len(beam[0x300a,0x03a8][0][0x300a,0x0396].value)):
        if spot_number % 2 == 1 and offset_spot:
            beam[0x300a,0x03a8][0][0x300a,0x0396].value[spot_number] = int(mu_per_offset_spot_list[i]/2)

    beam[0x300a,0x03a8][1][0x300a,0x0396].value = N_spots_list[i]*[0]
    beam[0x300a,0x00c2].value = f"E{energy_list[i]}_F{int(x_field_list[i]/10)}x{int(y_field_list[i]/10)}_OX{field_offset_x_list[i]/10}_OY{field_offset_y_list[i]/10}_MU{mu_per_spot_list[i]}"
    beam[0x300a,0x03a8][0][0x300a,0x11e].value = 270
    #beam[0x]Gantry angle 270]
    i+=1

i=0
total_dose = 0
for beam in reference_beam_sequence:
    beam[0x300a,0x0086].value =2*mu_list[i]
    beam[0x300a,0x0084].value = dose_list[i]
    total_dose+=dose_list[i]
    i+=1


#set total dose
dcm[0x300a,0x0010][0][0x300a,0x0026].value = total_dose
end_string = "no_offset"
if offset_spot:
    end_string ="offset_150"
filename = sys.argv[3]

#gernerate file path
path = sys.argv[1].split('/')
path.pop(-1)
path = '/'.join(path)

now = datetime.now()

dt_string = now.strftime("%Y_%m_%d_H_%M_%S")
dcm[0x300a,0x0002].value = dt_string
dcm[0x0008,0x103e].value =dt_string

tolerance_table = dcm[0x300a,0x03a0][0]
tolerance_table[0x300a,0x0042].value = 1
tolerance_table[0x300a,0x0043].value = 'PBT_QA'
tolerance_table[0x300a,0x0044].value = 1
tolerance_table[0x300a,0x004b].value = 10.0
tolerance_table[0x300a,0x004c].value = 95
tolerance_table[0x300a,0x004f].value = 5.0
tolerance_table[0x300a,0x0050].value = 5.0
tolerance_table[0x300a,0x0051].value = 500
tolerance_table[0x300a,0x0052].value = 1500
tolerance_table[0x300a,0x0053].value = 500

dcm[0x300e,0x0002].value = "APPROVED"
dcm.save_as(path+'/'+filename)
