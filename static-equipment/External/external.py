
from typing import Literal


class External:
    def __init__(
        self,
        r: float,
        t: float,
        sweeping_angle: Literal[15, 30, 60, 90, 120, 150, 180],
        elasticity: float,
        poisson: float,
    ):
        self.r = r  # radius of curvature
        self.t = t  # thickness in inches
        self.sweeping_angle = sweeping_angle
        self.elasticity = elasticity
        self.poisson = poisson

        a_k_dict = {
            15: 17.2,
            30: 8.62,
            60: 4.37,
            90: 3.0,
            120: 2.36,
            150: 2.07,
            180: 2.0,
        }

        self.k_value = a_k_dict[self.sweeping_angle]

    def p_prime(self):
        return (
            self.elasticity
            * (self.t ** 3)
            * (self.k_value ** 2 - 1)
        ) / ((12 * (self.r ** 3)) * (1 - self.poisson ** 2))


instance1 = External(15, 0.340, 30, 30000, 0.5)
allowable_pressure = instance1.p_prime() / 3

print(f"Maximum allowable test pressure is {allowable_pressure}")







