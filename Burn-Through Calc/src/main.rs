use std::f64::consts::{E, PI};

struct Parameters {
    t_process: f64,
    t_0: f64,
    t_m: f64,
    rho_c: f64,
    h: f64,
    f: f64,
    e: f64,
    i: f64,
    v: f64,
    cpt: f64,
    wb: f64,
}

fn main() {
   
    let params = Parameters {
        t_process: 400.0,  // Process temperature (°F)
        t_0: 70.0,         // Initial temperature (°F)
        t_m: 2750.0,       // Melting temperature (°F) - CS=2750, SS=2550
        rho_c: 40.0,       // Volumetric specific heat (J/in³·°F) - CS & SS = 40
        h: 0.375,          // Wall thickness (inches)
        f: 0.7,            // Arc efficiency - GTAW=0.4, SMAW=0.7
        e: 24.0,           // Voltage (V) - E7018=24, E7016=23, ER70S-2=20
        i: 120.0,          // Current (A) - E7018=120, E7016=100, ER70S-2=110
        v: 10.0,           // Travel speed (in/min)
        cpt: 1800.0,       // Critical peak temperature (°F)
        wb: 0.079,         // Weld bead depth (in) - SMAW=0.079, GTAW=0.039
    };
    
    
    let h_net = calculate_net_heat_input(params.f, params.e, params.i, params.v);
    let haz = calculate_haz_penetration(h_net, params.rho_c, params.h, params.t_0, params.t_m, params.cpt);
    let total_penetration = haz + params.wb;
    let t_inside = peak_temperature(params.h, h_net, params.rho_c, params.h, params.t_m, params.t_0);
    let safe_to_weld = total_penetration < params.h;
    
    
    print_results(&params, h_net, haz, total_penetration, t_inside, safe_to_weld);
}

fn calculate_net_heat_input(f: f64, e: f64, i: f64, v: f64) -> f64 {
    f * e * i * 60.0 / v
}

fn peak_temperature(y: f64, h_net: f64, rho_c: f64, h: f64, t_m: f64, t_0: f64) -> f64 {
    let numerator = (2.0 * PI * E).sqrt() * rho_c * h * y;
    let term1 = numerator / h_net;
    let term2 = 1.0 / (t_m - t_0);
    1.0 / (term1 + term2) + t_0
}

fn calculate_haz_penetration(h_net: f64, rho_c: f64, h: f64, t_0: f64, t_m: f64, cpt: f64) -> f64 {
    let term1 = 1.0 / (cpt - t_0);
    let term2 = 1.0 / (t_m - t_0);
    let denominator = (2.0 * PI * E).sqrt() * h * rho_c;
    (term1 - term2) * h_net / denominator
}

fn print_results(params: &Parameters, h_net: f64, haz: f64, total_penetration: f64, t_inside: f64, safe_to_weld: bool) {
    println!("{}", "=".repeat(60));
    println!("WELD PEAK TEMPERATURE ANALYSIS");
    println!("{}", "=".repeat(60));
    
    println!("\nInput Parameters:");
    println!("  Process Temperature: {:.1}°F", params.t_process);
    println!("  Initial Temperature: {:.1}°F", params.t_0);
    println!("  Melting Temperature: {:.1}°F", params.t_m);
    println!("  Volumetric Specific Heat: {:.1} J/in³·°F", params.rho_c);
    println!("  Wall Thickness: {:.3} in", params.h);
    println!("  Arc Efficiency: {:.1}", params.f);
    println!("  Voltage: {:.1} V", params.e);
    println!("  Current: {:.1} A", params.i);
    println!("  Travel Speed: {:.1} in/min", params.v);
    println!("  Critical Peak Temperature: {:.1}°F", params.cpt);
    println!("  Weld Bead Depth: {:.3} in", params.wb);
    
    println!("\nCalculated Values:");
    println!("  Net Heat Input: {:.2} J/min", h_net);
    println!("  HAZ Penetration: {:.4} in", haz);
    println!("  Total Penetration (HAZ + Weld Bead): {:.4} in", total_penetration);
    println!("  Wall Thickness: {:.4} in", params.h);
    
    println!("\n{}", "=".repeat(60));
    if safe_to_weld {
        println!(" PASS: Welding operation is feasible");
        println!("  Critical peak temperature does not reach inside wall");
        let margin = params.h - total_penetration;
        println!("  Safety Margin: {:.4} in ({:.2}%)", margin, (margin / params.h) * 100.0);
    } else {
        println!(" FAIL: Welding operation is not feasible");
        println!("  Critical peak temperature reaches inside wall");
        let exceedance = total_penetration - params.h;
        println!("  Exceedance: {:.4} in", exceedance);
    }
    println!("{}", "=".repeat(60));
    
    println!("\nTemperature at Inside Wall: {:.1}°F", t_inside);
}


