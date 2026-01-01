from dataclasses import dataclass
from typing import Literal
import numpy as np

from .util import ANTONINE_COEFFICIENTS


@dataclass
class NPSHA:

    Pvap_type: Literal["upper", "lower"] = "upper"

    Pvap_upper: float = 46.33
    Pvap_lower: float = 6.45

    specific_gravity: float = 0.569
    P_abs: float = 56.7  # psia
    water_density: float = 1000.0

    hst: float = 5
    hfs: float = 4.9

    water_head_factor: float = 2.31

    @property
    def Pvap(self) -> float:
        """Returns Pvap_upper or Pvap_lower based on Pvap_type."""
        if self.Pvap_type == "upper":
            return self.Pvap_upper
        return self.Pvap_lower

    def hp(self):
        return (self.P_abs * self.water_head_factor) / self.specific_gravity

    def hvpa(self) -> float:
        """Calculate hvpa using the selected Pvap (upper or lower)."""
        return (self.Pvap * self.water_head_factor) / self.specific_gravity


if __name__ == "__main__":

     
    _1_3_Butadiene = ANTONINE_COEFFICIENTS("1,3-Butadiene", 3.99979, 941.662, -32.753, 100, 310.92, 0.6)
    _1_Butene = ANTONINE_COEFFICIENTS("1-Butene", 4.24696, 1099.207, -8.256, 100, 310.92, 0.1)
    _n_Pentane = ANTONINE_COEFFICIENTS("n-Pentane", 3.9892, 1070.917, -40.454, 100, 310.92, 0.3)

    antonine_pressures = [_1_3_Butadiene.pressure_bar(), _1_Butene.pressure_bar(), _n_Pentane.pressure_bar()]

    
    total_vapor_pressure = (
        _1_3_Butadiene.pressure_bar() * _1_3_Butadiene.comp +
        _1_Butene.pressure_bar() * _1_Butene.comp +
        _n_Pentane.pressure_bar() * _n_Pentane.comp
    )

    npsha_upper = NPSHA("upper")
    npsha_lower = NPSHA("lower")

    print(f"Antoine pressures (bar): {antonine_pressures}")
    print(f"Total vapor pressure (bar): {total_vapor_pressure}")
    print(f"Upper - Pvap: {npsha_upper.Pvap}, hvpa: {npsha_upper.hvpa()}")
    print(f"Lower - Pvap: {npsha_lower.Pvap}, hvpa: {npsha_lower.hvpa()}")


	
