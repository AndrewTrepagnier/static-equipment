"""
Burn-Through (Hot Tap) Weld Peak Temperature Calculator

Calculates the temperature profile through a pipe/vessel wall during welding
on live equipment. The acceptance criterion is that the critical peak
temperature (e.g. 1800 F for E7018) must NOT reach the inside wall surface,
i.e.  HAZ + Weld Bead Depth < Wall Thickness.

Equations (no heat removal assumption):
    H_net   = f * E * I * 60 / v                                        (J/min)
    Tp(y)   = 1 / ( (sqrt(2*pi*e) * rhoC * h * y) / H_net
                    + 1/(Tm - T0) ) + T0                                ( F)
    HAZ     = (1/(CPT - T0) - 1/(Tm - T0)) * H_net /
              (sqrt(2*pi*e) * rhoC * h)                                 (inches)

Edit the `inputs` dictionary below, then run:
    python burn_through_calc.py
"""

import math
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# INPUTS  --  edit values here
# ---------------------------------------------------------------------------
inputs = {
    # Job identification (free-form text, used in the plot title)
    "calculated_by": "A. Trepanier",
    "moc_or_job":    "MOC-0000",
    "process":       "Example process",
    "material":      "Carbon Steel",
    "location":      "Tie-in on 6-inch line",

    # Process / geometry
    "T_process":  90.0,    # process fluid temperature, F  (note: <=212 F if H2 service)
    "T0":         75.0,    # uniform initial temperature, F (ambient if no preheat)
    "Tm":       2750.0,    # steel melting temperature,  F  (CS=2750, SS=2550)
    "rhoC":       40.0,    # volumetric specific heat, J/in^3/F (CS & SS ~ 40)
    "h":           0.144,  # parent wall thickness, inches

    # Welding parameters
    "f":           0.7,    # arc efficiency  (GTAW=0.4, SMAW=0.7)
    "E":          24.0,    # voltage, V      (E7018=24, E7016=23, ER70S-2=20)
    "I":         120.0,    # current, A      (E7018=120, E7016=100, ER70S-2=110)
    "v":           6.0,    # travel speed, in/min  ** critical parameter **
    "CPT":      1800.0,    # critical peak temperature, F (E7018/E7016/ER70S-2=1800, E6010=1400)
    "wb":          0.079,  # weld bead depth into wall, in (SMAW=0.079, GTAW=0.039)
}


# ---------------------------------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------------------------------
def net_heat_input(f, E, I, v):
    """H_net in J/min."""
    return f * E * I * 60.0 / v


def peak_temperature(y, H_net, rhoC, h, Tm, T0):
    """Peak temperature in HAZ at distance y from the fusion line ( F)."""
    y = np.asarray(y, dtype=float)
    coeff = math.sqrt(2.0 * math.pi * math.e)
    with np.errstate(divide="ignore", invalid="ignore"):
        denom = (coeff * rhoC * h * y) / H_net + 1.0 / (Tm - T0)
        Tp = 1.0 / denom + T0
    Tp = np.where(y <= 0.0, Tm, Tp)
    return Tp


def haz_depth(H_net, rhoC, h, Tm, T0, CPT):
    """Distance from fusion line where Tp equals the critical peak temp."""
    coeff = math.sqrt(2.0 * math.pi * math.e)
    return (1.0 / (CPT - T0) - 1.0 / (Tm - T0)) * H_net / (coeff * rhoC * h)


H_net  = net_heat_input(inputs["f"], inputs["E"], inputs["I"], inputs["v"])
HAZ    = haz_depth(H_net, inputs["rhoC"], inputs["h"],
                   inputs["Tm"], inputs["T0"], inputs["CPT"])
total  = HAZ + inputs["wb"]
margin = inputs["h"] - total
T_id   = float(peak_temperature(inputs["h"], H_net, inputs["rhoC"],
                                inputs["h"], inputs["Tm"], inputs["T0"]))
safe   = total < inputs["h"]


# ---------------------------------------------------------------------------
# CONSOLE OUTPUT
# ---------------------------------------------------------------------------
bar = "=" * 60
print(bar)
print("BURN-THROUGH / WELD PEAK TEMPERATURE ANALYSIS")
print(bar)
print(f"  Job:           {inputs['moc_or_job']}  ({inputs['calculated_by']})")
print(f"  Process:       {inputs['process']}")
print(f"  Material:      {inputs['material']}")
print(f"  Location:      {inputs['location']}")
print("\nResults:")
print(f"  Net heat input H_net        : {H_net:>10.1f} J/min")
print(f"  HAZ penetration             : {HAZ:>10.4f} in")
print(f"  Weld bead depth             : {inputs['wb']:>10.4f} in")
print(f"  Total (HAZ + weld bead)     : {total:>10.4f} in")
print(f"  Wall thickness              : {inputs['h']:>10.4f} in")
print(f"  Remaining wall (ID side)    : {margin:>10.4f} in")
print(f"  Peak temp at inside wall    : {T_id:>10.1f}  F")
print(bar)
verdict = "PASS  -  welding feasible" if safe else "FAIL  -  burn-through risk"
print(f"  {verdict}")
print(bar)


# ---------------------------------------------------------------------------
# PLOT  --  one panel, one story:
#   The red curve is the peak temperature through the wall (depth from OD).
#   The grey line is the 1800 F critical threshold.
#   The blue line is the inside wall.
#   The red dot is where 1800 F lands in the wall.
#   If the red dot is LEFT of the blue line  ->  safe.
# ---------------------------------------------------------------------------
x_cpt = inputs["wb"] + HAZ                       # depth from OD where Tp = CPT
xmax  = max(inputs["h"], x_cpt) * 1.15
x     = np.linspace(0.0, xmax, 500)

y_from_fl = x - inputs["wb"]
Tp = peak_temperature(np.maximum(y_from_fl, 1e-9),
                      H_net, inputs["rhoC"], inputs["h"],
                      inputs["Tm"], inputs["T0"])
Tp = np.where(x <= inputs["wb"], inputs["Tm"], Tp)   # weld bead is molten

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(x, Tp, color="#b22222", lw=2.5, zorder=3)

ax.axhline(inputs["CPT"], color="#666", ls="--", lw=1.0, zorder=1)
ax.text(xmax * 0.995, inputs["CPT"] + 35,
        f"{inputs['CPT']:.0f} F critical",
        ha="right", va="bottom", color="#666", fontsize=9)

ax.axvline(inputs["h"], color="#1f4e79", ls="--", lw=1.2, zorder=1)
ax.text(inputs["h"] + 0.004, inputs["Tm"] * 0.55,
        f"inside wall\nh = {inputs['h']:.3f}\"",
        color="#1f4e79", fontsize=9, va="center")

# Red dot - the only callout
ax.plot([x_cpt], [inputs["CPT"]],
        "o", color="red", ms=14, mec="white", mew=2, zorder=10)
ax.annotate(f"{x_cpt:.3f}\" from OD",
            xy=(x_cpt, inputs["CPT"]),
            xytext=(x_cpt + 0.04, inputs["CPT"] + 550),
            fontsize=11, color="red", fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="red", lw=1.4))

ax.set_xlim(0, xmax)
ax.set_ylim(0, inputs["Tm"] * 1.05)
ax.set_xlabel("Depth from OD (inches)")
ax.set_ylabel("Peak temperature ( F)")

verdict       = "PASS" if safe else "FAIL"
verdict_color = "#1b6e1b" if safe else "#a40000"
ax.set_title(
    f"Burn-Through:  {verdict}     "
    f"HAZ + bead = {total:.3f}\" of {inputs['h']:.3f}\" wall     "
    f"margin = {margin:+.3f}\"",
    color=verdict_color, fontsize=12, fontweight="bold",
)

ax.grid(True, alpha=0.25)
plt.tight_layout()
plt.show()
