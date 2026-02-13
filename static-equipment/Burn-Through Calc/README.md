# Weld Peak Temperature Calculations for Welding on Live Equipment (Hot Taps)

## Overview

The feasibility of safely performing live welding operations on an in-service pipe/vessel is governed by three potential risks:

- **Fluid Decomposition** - Process fluid breaking down due to excessive heat
- **Fluid Autoignition** - Process fluid igniting from high temperatures
- **Loss of Containment** - Burn-through of the vessel wall

This tool calculates the temperature profile through the wall during welding to determine if the operation can be performed safely. The key question: **Does the critical peak temperature penetrate through to the inside wall where it would contact the process fluid?**

## Acceptance Criteria

Welding on live equipment is generally considered feasible if:
- The critical peak temperature (1800°F for E7018, E7016, and ER70S-2 electrodes) does **NOT** reach the inside wall surface
- The inside wall temperature remains below the fluid's decomposition temperature
- The inside wall temperature remains below the fluid's autoignition temperature

The tool performs this check: **HAZ + Weld Bead Depth < Wall Thickness**

## Input Parameters

Edit these values directly in `src/main.rs`:

| Parameter | Description | Units | Typical Values |
|-----------|-------------|-------|----------------|
| `t_process` | Process fluid temperature | °F | - |
| `t_0` | Uniform initial temperature | °F | Ambient (70°F) |
| `t_m` | Steel melting temperature | °F | CS=2750, SS=2550 |
| `rho_c` | Volumetric specific heat capacity | J/in³·°F | CS & SS = 40 |
| `h` | Parent wall thickness | inches | - |
| `f` | Arc efficiency | - | GTAW=0.4, SMAW=0.7 |
| `e` | Voltage | volts | E7018=24, E7016=23, ER70S-2=20 |
| `i` | Current | amps | E7018=120, E7016=100, ER70S-2=110 |
| `v` | **Travel speed**  | in/min | **Critical parameter** |
| `cpt` | Critical peak temperature | °F | 1800 |
| `wb` | Weld bead penetration depth | inches | SMAW=0.079, GTAW=0.039 |

## Calculation Methodology

### Step 1: Net Heat Input

Calculate the net heat energy entering the weld per unit length:

$$
H_{net} = \frac{f \cdot E \cdot I \cdot 60}{v}
$$

Where:
- $f$ = arc efficiency (fraction of arc energy that heats the metal)
- $E$ = voltage (volts)
- $I$ = current (amps)
- $v$ = travel speed (in/min)
- Result is in J/min

### Step 2: Peak Temperature Profile

Calculate the peak temperature at distance $y$ from the fusion line:

$$
T_p(y) = \left( \frac{ \sqrt{2\pi e} \cdot \rho C \cdot h \cdot y }{ H_{net} } + \frac{1}{T_m - T_0} \right)^{-1} + T_0
$$

Where:
- $y$ = distance from fusion line (inches), where $y=0$ is at the fusion line
- $e$ = Euler's number (2.71828...)
- $\rho C$ = volumetric specific heat capacity
- $h$ = wall thickness
- $T_m$ = melting temperature
- $T_0$ = initial temperature

### Step 3: HAZ Penetration at Critical Temperature

Find the distance where the peak temperature equals the critical peak temperature:

$$
HAZ = \left( \frac{1}{CPT - T_0} - \frac{1}{T_m - T_0} \right) \cdot \frac{H_{net}}{\sqrt{2\pi e} \cdot h \cdot \rho C}
$$

### Step 4: Pass/Fail Check

The total heat penetration is:

$$
\text{Total Penetration} = HAZ + wb
$$

**Pass:** Total Penetration < Wall Thickness  
**Fail:** Total Penetration ≥ Wall Thickness

## Usage

1. Edit the parameter values at the top of `src/main.rs`
2. Run the calculator:
   ```bash
   cargo run --release
   ```


