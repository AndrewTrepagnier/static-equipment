from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class ANTONINE_COEFFICIENTS:

    name: str

    A: float
    B: float
    C: float

    Temp_F: float
    Temp_K: float

    comp: float

    def log_p(self):
        return self.A - (self.B / (self.Temp_K + self.C))

    def pressure_bar(self):
        return 10 ** self.log_p()
