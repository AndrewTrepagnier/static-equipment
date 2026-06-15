



class Horizontal_weld:



    def __init__(self, longitudinal_distance, normal_force, elastic_const, 
                 plate_length, plate_width, load_location, weld_leg, weld_spacing):


        self.normal_force = normal_force
        self.longitudinal_distance = longitudinal_distance # denoted as c in bending stress equation
        self.elastic_const = elastic_const
        self.plate_length = plate_length
        self.plate_width = plate_width  # weld length
        self.load_location = load_location # distance from load to weld
        self.weld_leg = weld_leg     # fillet weld size
        self.weld_spacing = weld_spacing  # distance between top and bottom welds


    def weld_throat(self):
        # throat = 0.707 * weld leg

        throat = 0.707 * self.weld_leg

        return throat


    def weld_area(self):

        # Area of one weld throat

        weld_area = self.weld_throat() * self.plate_width

        return weld_area


    def bending_moment(self):

		# beinding moment is the resultant load times the distance from the load to the point of interest, q.
		# maximum bending moment occurs when a = 0 (distance of the load to the free end)for the equation

        self.bending_moment = self.normal_force * self.load_location

        return self.bending_moment


    def moment_area_intertia(self):

        # Weld group moment of inertia
        #
        # I = sum(A*d^2)
        #
        # Two welds located above and below neutral axis
        # d = weld_spacing/2

        d = self.weld_spacing / 2

        I_wl = 2 * self.weld_area() * d**2

        return I_wl


    def bending_stress(self):

        # Note: bending stress in the fillet is really just secondary shear on the throat, not plate bending stress, however, the math is still right for fillet weld checks.

        self.longitudinal_distance = self.weld_spacing / 2

        return (self.bending_moment() * self.longitudinal_distance) / self.moment_area_intertia()


    def shear_stress(self):

        # Direct shear stress from applied force
        #
        # tau = V/A

        total_weld_area = 2 * self.weld_area()

        return self.normal_force / total_weld_area


    def resultant_stress(self):

        # Combine bending and direct shear

        bending = self.bending_stress()
        shear = self.shear_stress()

        return (bending**2 + shear**2)**0.5

