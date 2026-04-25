# -*- coding: utf-8 -*-
"""
Main Power Flow Script
"""
from pathlib import Path
import PowerFlow_46705_sol as pf  # import Power Flow functions
import LoadNetworkData_sol as lnd     # load the network data to global variables

# Power flow settings
max_iter = 30   # Iteration settings
err_tol = 1e-6  # Specify error tolerance
# Load the Network data ...
# filename = "./Network_Data/Assignment_1_LL.txt" # set the correct path to the system .txt file
base_dir = Path(__file__).resolve().parent
filename = base_dir / "Network_Data" / "Assignment_1_LL.txt"

lnd.LoadNetworkData(filename) # makes Ybus available as lnd.Ybus etc.


# Carry out the power flow analysis ...
V,success,n = pf.PowerFlowNewton(lnd.Ybus,lnd.Sbus,lnd.V0,lnd.pv_index,lnd.pq_index,max_iter,err_tol,print_progress=True)
# Display results if the power flow analysis converged
if success:
    pf.DisplayResults_and_loading(V,lnd)    
    violations = pf.System_violations(V,lnd)
    if not violations: #no violations, print status and move on
        print('\n-----------------------Limits OK!------------------------\n')
    else: # if violation, display them
        print('\n-----------------------Violations!-----------------------\n')
        for str_ in violations:
            print(str_)
