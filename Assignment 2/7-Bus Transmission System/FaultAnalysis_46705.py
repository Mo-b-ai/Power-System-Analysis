"""
46705 - Power Grid Analysis
This file contains the definitions of the functions needed to
carry out Fault Analysis calculations in python.
"""

import numpy as np

# 1. the FaultAnalysis() function
def FaultAnalysis(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,fault_type,Zf,Vf):
   
    # calculate sequence fault currents
    Iseq = Calculate_Sequence_Fault_Currents(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,fault_type,Zf,Vf)
    # calculate sequence fault voltages
    Vseq_mat = Calculate_Sequence_Fault_Voltages(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,Vf,Iseq)
    # convert sequence currents to phase (fault) currents
    Iph = Convert_Sequence2Phase_Currents(Iseq)
    # convert sequence voltages to phase line-to-ground (fault) voltages
    Vph_mat = Convert_Sequence2Phase_Voltages(Vseq_mat)    
    return Iph, Vph_mat

# 1.1. the Calculate_Sequence_Fault_Currents() function
def Calculate_Sequence_Fault_Currents(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,fault_type,Zf,Vf):
#  fault_type: 0 = 3-phase balanced fault; 1 = Single Line-to-Ground fault;
#              2 = Line-to-Line fault;     3 = Double Line-to-Ground fault.    
    # Iseq current array: 
    # Iseq[0] = zero-sequence; Iseq[1] = positive-sequence; Iseq[2] = negative-sequence
    fb = bus_to_ind[fault_bus]
    Z0=Zbus0[fb,fb]
    Z1=Zbus1[fb,fb]
    Z2=Zbus2[fb,fb]
    Iseq = np.zeros(3,dtype=complex)
    if fault_type == 0:
        Iseq[1]=Vf/(Z1+3*Zf) #edit: three phase bolted short circuit fault (no ground imepedance)
    elif fault_type == 1:
        Iseq[0]=Vf/(Z0+Z1+Z2+3*Zf) #edit: line to ground with ground impedance
        Iseq[1]=Iseq[0]
        Iseq[2]=Iseq[0]
    elif fault_type == 2:
        Iseq[1]=Vf/(Z1+Z2) #edit: Line to line fault
        Iseq[2]=-Iseq[1]
    elif fault_type == 3:
        Iseq[1]=Vf/(Z1+(Z2*(Z0+3*Zf))/(Z2+(Z0+3*Zf))) #edit: Double line to ground fault
        Iseq[2]=-Iseq[1]*((Z0+3*Zf)/(Z0+Z2+3*Zf))
        Iseq[0]=-Iseq[1]*Z2/(Z0+Z2+3*Zf)
    else:
        print('Unknown Fault Type')
    return Iseq

# 1.2 the Calculate_Sequence_Fault_Voltages() function
def Calculate_Sequence_Fault_Voltages(Zbus0,Zbus1,Zbus2,bus_to_ind,fault_bus,Vf,Iseq):
    fb = bus_to_ind[fault_bus]
    # Initialize Vseq as a zero matrix of size Nx3
    Vseq_mat = np.zeros((Zbus0.shape[0], 3), dtype=complex)
    # Multiply only the n’th column of Z by Iseq[n]
    Vseq_mat[:, 0] = -Iseq[0] * Zbus0[:, fb]
    Vseq_mat[:, 1] = Vf - Iseq[1] * Zbus1[:, fb]
    Vseq_mat[:, 2] = -Iseq[2] * Zbus2[:, fb]

    return Vseq_mat

# 1.3. the Convert_Sequence2Phase_Currents() function
def Convert_Sequence2Phase_Currents(Iseq):
    
    # Define the transformation matrix
    a = np.exp(1j * 2 * np.pi / 3)
    T = np.array([
    [1, 1, 1],
    [1, a**2, a],
    [1, a, a**2]
    ])

    # Convert to phase currents

    Iph=Iseq @ T

    return Iph

# 1.4 the Convert_Sequence2Phase_Voltages() function
def Convert_Sequence2Phase_Voltages(Vseq_mat):
    
    # Define the transformation matrix
    a = np.exp(1j * 2 * np.pi / 3)
    T = np.array([
    [1, 1, 1],
    [1, a**2, a],
    [1, a, a**2]
    ])

    # Convert to phase voltages
    Vph_mat = Vseq_mat @ T.T  

    return Vph_mat

# ####################################################
# #  Displaying the results in the terminal window   #
# ####################################################
# 2. the DisplayFaultAnalysisResults() function

fault_messages = [
    "3-phase balanced fault                                      ",
    "Single Line-to-Ground fault, phase a                        ",
    "Line-to-Line fault, phase b + c                             ",
    "Double Line-to-Ground fault, phase b + c                    "
]

def DisplayFaultAnalysisResults(Iph,Vph_mat,fault_bus,fault_type,Zf,Vf):
    print('==============================================================')
    print('|                  Fault Analysis Results                    |')
    print('==============================================================')
    print('|'+ fault_messages[fault_type] +'|')
    print(f'|Prefault Voltage: Vf=  {Vf:5.3f}pu                              |')
    print(f'|Fault Impedance:  Zf=  {Zf:5.3f}pu                              |')
    print('==============================================================')  
    print('|Phase Currents:---------------------------------------------|')
    print('|-------------                                               |')
    print('|     ---- Phase a ----| ---- Phase b ----| ---- Phase c ----|')
    print('|     -----------------|------------------|------------------|')
    print('|      Mag(pu) Ang(deg)|  Mag(pu) Ang(deg)|  Mag(pu) Ang(deg)|')
    print(f'|       {np.abs(Iph[0]):<8.3f}{np.degrees(np.angle(Iph[0])):<7.2f}|   {np.abs(Iph[1]):<8.3f}{np.degrees(np.angle(Iph[1])):<7.2f}|   {np.abs(Iph[2]):<8.3f}{np.degrees(np.angle(Iph[2])):<7.2f}|')
    print('==============================================================')  
    print('|Phase Line to Ground Voltages:------------------------------|')
    print('|-----------------------------                               |')
    print('|   | ---- Phase a ----| ---- Phase b ----| ---- Phase c ----|')
    print('|Bus|------------------|------------------|------------------|')
    print('|   |  Mag(pu) Ang(deg)|  Mag(pu) Ang(deg)|  Mag(pu) Ang(deg)|')
    print('|---| -------- ------- | -------- ------- | -------- ------- |')
    for i in range(len(Vph_mat)):
        print(f'| {i+1:<2}|   {np.abs(Vph_mat[i,0]):<8.3f}{np.degrees(np.angle(Vph_mat[i,0])):<7.2f}|   {np.abs(Vph_mat[i,1]):<8.3f}{np.degrees(np.angle(Vph_mat[i,1])):<7.2f}|   {np.abs(Vph_mat[i,2]):<8.3f}{np.degrees(np.angle(Vph_mat[i,2])):<7.2f}| ')
    print('==============================================================')  
    return