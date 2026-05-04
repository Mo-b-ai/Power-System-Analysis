# -*- coding: utf-8 -*-
"""
Security Analysis Script
"""
from pathlib import Path
import numpy as np
import PowerFlow_46705 as pf  # import Power Flow functions
import LoadNetworkData as lnd     # load the network data to global variables
max_iter = 30   # Iteration settings
err_tol = 1e-3
# Load the Network data ...
base_dir = Path(__file__).resolve().parent
filename = base_dir / "Network_Data" / "BaseCase+Line2-4.txt"

lnd.LoadNetworkData(filename) # makes Ybus available as lnd.Ybus etc.

def System_violations(V,Ybus,Y_from,Y_to,lnd):
    # Inputs: 
    # V = results from the load flow
    # Ybus = the bus admittance matrix used in the load flow
    # Y_from,Y_to = tha admittance matrices used to determine the branch flows
    # lnd = the LoadNetworkData object for easy access to other model data
    
    #store variables as more convenient names
    br_f=lnd.br_f; br_t=lnd.br_t;   #from and to branch indices 
    ind_to_bus=lnd.ind_to_bus;      # the ind_to_bus mapping object    
    bus_to_ind=lnd.bus_to_ind;      # the bus_to_ind mapping object    
    br_MVA = lnd.br_MVA             # object containing the MVA ratings of the branches 
    br_id  = lnd.br_id              # (you have to update LoadNetworkData for this) 


    #line flows and generators injection....
    S_to = V[br_t]*(Y_to.dot(V)).conj()         # the flow in the to end..
    S_from = V[br_f]*(Y_from.dot(V)).conj()     # the flow in the from end
    S_inj = V*(Ybus.dot(V)).conj()              # the injected power 
    SLD=lnd.S_LD                                # The defined loads on the PQ busses
    S_gen = S_inj + SLD                         # the generator arrays
    
    gen_ind = np.where(lnd.buscode>1)[0] #find the generator nodes
    gen_str = ' --> Generator at bus {:} overloaded ({})'
    violations = []
    
   ##################################################################################
   # YOUR CODE COMES HERE:
   # 1. Check flow in all branches (both ends) and report if limits are violated
    br_str = ' --> Branch #{:} - from bus {:} to bus {:} (ID:{:}) overloaded (fr:{:.2f}%, to:{:.2f}%)'
    for i,fr,to,MVA in zip(range(len(br_f)),br_f,br_t,br_MVA):
        fr_loading = np.abs(S_from[i]*lnd.MVA_base/MVA)    
        to_loading = np.abs(S_to[i]*lnd.MVA_base/MVA)    
        if ((fr_loading > 1)|(to_loading > 1)):
            br_nr = i+1
            violations.append(br_str.format(br_nr,ind_to_bus[fr], ind_to_bus[to], br_id[i] ,fr_loading*100,to_loading*100))
    
   # 2. Check output of all generators and see if limits are exceeded
    for g in gen_ind:
        g_loading = np.abs(S_gen[g])*lnd.MVA_base/lnd.Gen_MVA[g]
        pgen = np.real(S_gen[g])*lnd.MVA_base
        qgen = np.imag(S_gen[g])*lnd.MVA_base
        bus_nr = lnd.ind_to_bus[g]
        pmax = lnd.p_gen_max[g]*lnd.MVA_base
        qmax = lnd.q_gen_max[g]*lnd.MVA_base
        qmin = lnd.q_gen_min[g]*lnd.MVA_base
        if g_loading > 1.0001: #if gen violation, record it
            errtype = 'Loading = {:.2f}  [%]'.format(g_loading*100)
            violations.append(gen_str.format(bus_nr,errtype))
        if pgen / pmax > 1.0001:
            errtype = 'Pgen = {:.2f} > {:.2f} [MW]'.format(pgen,pmax)
            violations.append(gen_str.format(bus_nr,errtype))
        if qgen > qmax:
            errtype = 'Qgen = {:.2f}  > {:.2f} [MVAr]'.format(qgen,qmax)
            violations.append(gen_str.format(bus_nr,errtype))
        if qgen < qmin:
            errtype = 'Qgen = {:.2f}  < {:.2f} [MVAr]'.format(qgen,qmin)
            violations.append(gen_str.format(bus_nr,errtype))
   # 3. Check voltages on all busses and see if it remains within pre-defined bounds
    ind_low = np.where(np.abs(V)< lnd.v_min)
    ind_high = np.where(np.abs(V)> lnd.v_max)

    V_h_str = ''
    for ind_h in ind_high[0]:
        V_h_str += '\n      Bus {:<4} ->  {:.3f} pu > V_max: {:.3f} pu'.format(lnd.ind_to_bus[ind_h],np.abs(V[ind_h]),lnd.v_max[ind_h])    

    V_l_str = ''
    for ind_l in ind_low[0]:
        V_l_str += '\n      Bus {:<4} ->  {:.3f} pu < V_min: {:.3f} pu'.format(lnd.ind_to_bus[ind_l],np.abs(V[ind_l]),lnd.v_min[ind_l])    
   
    if len(ind_high[0])>0:
        volt_str = ' --> Voltages too high at ...' + V_h_str
        violations.append(volt_str)
    
    if len(ind_low[0])>0:
        volt_str = ' --> Voltages too low at ...' + V_l_str
        violations.append(volt_str)
   ##################################################################################
    
    return violations
    
    


def apply_contingency_to_Y_matrices(Ybus,Yfr,Yto,fr_ind,to_ind,br_ind,Ybr_mat):
    # input:
    # The original admittance matirces: Ybus,Yfr,Yto
    # The from and to end indices for the branch (fr_ind, to_ind)
    # The indice for where the branch is in the branch list (br_ind)
    # The 2x2 admittance matrix for the branch Ybr_mat
    ##########################################################
    # This is important, you must copy the original matrices
    Ybus_mod = Ybus . copy ( ) # otherwise you will change the original Ybus matrix
    Yfr_mod = Yfr . copy ( ) # when ever you make changes to Ybus_mod
    Yto_mod = Yto . copy ( ) # using the .copy() function avoids this
    ##################################################################################
    # YOUR CODE COMES HERE:
    # 1. Remove the branch from the Ybus_mod matrix
    ind_Ybus = np.array([fr_ind,to_ind]) #Find the correct place in the Ybus matrix.
    Ybus_mod[np.ix_(ind_Ybus,ind_Ybus)] -= Ybr_mat #Subtract the 2x2 matrix consisting of the branch admittance from the Ybus matrix.
    # 2. Remove the branch from the Yto and Yfr matrices
    Yfr_mod[br_ind,fr_ind] =  0     #Setting the from and to admi
    Yfr_mod[br_ind,to_ind] =  0
    Yto_mod[br_ind,to_ind] =  0       
    Yto_mod[br_ind,fr_ind] =  0
    ##################################################################################

    return Ybus_mod,Yfr_mod,Yto_mod






#%%
##############################################################
#   Part I:                                                  #
#   Study the base case and display results (with % loading) #
#                                                            #
##############################################################

# Carry out load flow of the base case.....
V,success,n = pf.PowerFlowNewton(lnd.Ybus,lnd.Sbus,lnd.V0,lnd.pv_index,lnd.pq_index,max_iter,err_tol)
if success: # Display results if the power flow analysis converged
    pf.DisplayResults_and_loading(V,lnd) 




#%% 
##############################################################
#    Part II:                                                #
#    Simplified contingency analysis (only branch outages)   #
#                                                            #
##############################################################

print('*'*50)
print('*             Contingency Analysis               *')
print('*'*50)


for i in range(len(lnd.br_f)): #sweep over branches
    fr_ind = lnd.br_f[i]
    to_ind = lnd.br_t[i]
    br_ind = i
    Ybr_mat = lnd.br_Ymat[i]
    Ybus_mod,Yfr_mod,Yto_mod = apply_contingency_to_Y_matrices(lnd.Ybus,lnd.Y_fr,lnd.Y_to,fr_ind,to_ind,br_ind,Ybr_mat)
    #        
    str_status = '---------------------------------------------------------------\nTripping of branch {:} (bus {:} - bus {:})'.format(i+1,lnd.ind_to_bus[fr_ind],lnd.ind_to_bus[to_ind])
        
    # Carry out load flow of the base case.....
    try:
        V,success,n = pf.PowerFlowNewton(Ybus_mod,lnd.Sbus,lnd.V0,lnd.pv_index,lnd.pq_index,max_iter,err_tol,print_progress=False)
    except:
        str_ = ' --> Load Flow error (Jacobian) when branch {:} (bus {:} - bus {:}) is tripped'.format(i+1,lnd.ind_to_bus[fr_ind],lnd.ind_to_bus[to_ind])
        print(str_status+ ' [CONVERGENCE ISSUES!]')
        print(str_)
    else:  
        if success: # Display results if the power flow analysis converged
            violations = System_violations(V,Ybus_mod,Yfr_mod,Yto_mod,lnd)
            if not violations: #no violations, print status and move on
                print(str_status + ' [OK!]')
            else: # if violation, display them
                print(str_status + ' [Violations!]')
                for str_ in violations:
                    print(str_)
        else: #no convergence...
            str_ = ' --> No load-flow convergence when branch {:} (bus {:} - bus {:}) is tripped'.format(i+1,lnd.ind_to_bus[fr_ind],lnd.ind_to_bus[to_ind])
            print(str_status + ' [CONVERGENCE ISSUES!]')
            print(str_)
    