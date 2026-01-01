
from dataclasses import dataclass
from typing import Optional
import numpy as np

from .util import ANTONINE_COEFFICIENTS




@dataclass
class NPSHA:

	Pvap_upper: float = 46.33
    Pvap_lower: float = 6.45
    
    specific_gravity: float = 0.569
    P_abs: 56.7 #psia 
    water_density: float = 1000.0 


    hst: float = 5
    hfs: float = 4.9  # 

    water_head_factor = 2.31


    antonine_list: Optional[list] = None
    


	def hp(self):

		return (P_abs*water_head_factor) / specific_gravity

	def hvpa(self, Pvap):

		return (Pvap*water_head_factor)/specific_gravity



if __name__=="__main__":

	_1_3_Budadeine = ANTONINE_COEFFICIENTS("1,3-Butadeine", 3.99979, 941.662, -32.753, 100, 310.92, 0.6)

	_1_Butene = ANTONINE_COEFFICIENTS("1-Butene", 4.24696, 1099.207, -8.256, 100, 310.92, 0.1)

	_n_Pentane = ANTONINE_COEFFICIENTS("n-Pentane", 3.9892, 1070.917, -40.454, 100, 310.92, 0.3)


	_1_3_Budadeine.log_p() 
	_1_3_Budadeine.pressure_bar().append(antonine_list)

	_1_Butene.log_p()
	_1_Butene.pressure_bar().append(antonine_list)

	_n_Pentane.log_p()
	_n_Pentane.pressure_bar().append(antonine_list)


	














