from dataclasses import dataclass
from typing import Optional
import numpy as np




@dataclass
class ANTOINES_COEFFICIENT:

	name: string

	A: float
	B: float
	C: float

	Temp_F: float
	Temp_K: float

	comp: float


	def log_p(self):

		return(A - (B/(Temp_K + C)))

	def pressure_bar(self, log_p):

		return 10**(log_p)





