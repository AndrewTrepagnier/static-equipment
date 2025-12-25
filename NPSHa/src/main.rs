use std::f64::consts::{E, PI};


struct Parameters {

	Pvap_upper: f64,
	Pvap_lower: f64,

	specific_g: f64,


	P_abs: f64, ///absolute pressure on the liquid surface (vapor space pressure)

	hst: f64, ///Static height of fluid relative to pump datum in feet, Positive if fluid is above the pump datum

	hfs: f64, /// Estimated frictional losses in suction line

	water_head_factor: f64, ///Use hp = (P_abs*2.31) / SG and hvpa = (Pvap*2.31)/SG
 
}

struct antoines_coefficients {

	Butadeine_1_3_A: f64,
	Butadeine_1_3_B: f64,
	Butadeine_1_3_C: f64,
	Butadeine_temp: f64, ///F


	Butene_1_A: f64,
	Butene_1_B: f64,
	Butene_1_C: f64,
	Butene_temp: f64, ///F

	Pentane_n_A: f64,
	Pentane_n_B: f64,
	Pentane_n_C: f64,
	Pentane_temp: f64, ///F

}



fn main(){

	let tk1_2_jumpover_inputs = Parameters{
		Pvap_upper: 46.33,
		Pvap_lower: 6.45,

		specific_g: 0.569,

		P_abs: 56.7,

		hst: 5,

		hfs: 4.9,

		water_head_factor: 2.31,

	}



fn F_to_K(F_temp: f64)->f64{
	((F_temp - 32)*5/9 + 273.15);
}


fn log_P(A:f64, B:f64, C:f64, Temp:f64)->f64{
	(A - (B)/(Temp + C));

}

fn compositions_pressures(){

}

fn vapor_pressure_mixture(){

}





	
}