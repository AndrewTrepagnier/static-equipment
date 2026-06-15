"""Tee-joint fillet weld strength from known plate stresses."""

import math


class FilletWeld:

    def __init__(
        self,
        plate_thickness,
        weld_leg_length,
        plate_direct_stress,
        plate_shear_stress,
        plate_bending_stress,
        allowable_stress=None,
    ):
        self.plate_thickness = float(plate_thickness)
        self.weld_leg_length = float(weld_leg_length)
        self.plate_direct_stress = float(plate_direct_stress)
        self.plate_shear_stress = float(plate_shear_stress)
        self.plate_bending_stress = float(plate_bending_stress)
        self.allowable_stress = (
            None if allowable_stress is None else float(allowable_stress)
        )

        if self.plate_thickness <= 0:
            raise ValueError("plate_thickness must be greater than zero")
        if self.weld_leg_length <= 0:
            raise ValueError("weld_leg_length must be greater than zero")
        if self.allowable_stress is not None and self.allowable_stress <= 0:
            raise ValueError("allowable_stress must be greater than zero")

    def weld_throat(self):
        return self.weld_leg_length / math.sqrt(2.0)

    def direct_shear_ratio(self):
        return self.weld_throat() / (2.0 * self.plate_thickness)

    def plate_section_modulus(self):
        t_p = self.plate_thickness
        return (t_p**3 / 12.0) / (t_p / 2.0)

    def weld_centroid_y(self):
        return (self.plate_thickness / 2.0 + self.weld_throat()) / 2.0

    def weld_section_modulus(self):
        return 2.0 * self.weld_throat() * self.weld_centroid_y()

    def bending_shear_ratio(self):
        return self.plate_section_modulus() / self.weld_section_modulus()

    def shear_from_direct(self):
        return abs(self.plate_direct_stress * self.direct_shear_ratio())

    def shear_from_plate_shear(self):
        return abs(self.plate_shear_stress * self.direct_shear_ratio())

    def shear_from_bending(self):
        return abs(self.plate_bending_stress * self.bending_shear_ratio())

    def in_plane_shear(self):
        return self.shear_from_direct() + self.shear_from_bending()

    def out_of_plane_shear(self):
        return self.shear_from_plate_shear()

    def total_shear(self):
        v_ip = self.in_plane_shear()
        v_oop = self.out_of_plane_shear()
        return math.sqrt(v_ip**2 + v_oop**2)

    def safety_factor(self):
        if self.allowable_stress is None:
            return None
        return self.allowable_stress / self.total_shear()

    def utilization(self):
        if self.allowable_stress is None:
            return None
        return self.total_shear() / self.allowable_stress

    def passes(self):
        if self.allowable_stress is None:
            return None
        return self.total_shear() <= self.allowable_stress

    def report(self, title="Tee/web-to-plate fillet weld"):
        print(f"Fillet weld: {title}")
        print(f"  t_p = {self.plate_thickness:.3f} in")
        print(f"  L_w = {self.weld_leg_length:.3f} in")
        print(f"  t_w = {self.weld_throat():.3f} in")
        print(f"  tau_wd = {self.shear_from_direct():.3f} psi")
        print(f"  tau_wp = {self.shear_from_plate_shear():.3f} psi")
        print(f"  tau_wb = {self.shear_from_bending():.3f} psi")
        print(f"  T_w    = {self.total_shear():.3f} psi")
        if self.allowable_stress is not None:
            verdict = "PASS" if self.passes() else "FAIL"
            print(f"  Allowable = {self.allowable_stress:.3f} psi")
            print(f"  SF        = {self.safety_factor():.2f}")
            print(f"  {verdict}")


def plot_fillet_weld(weld, title="Fillet weld"):
    """Optional sketch and stress table."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Arc, Circle, Polygon, Rectangle

    t_p = weld.plate_thickness
    L_w = weld.weld_leg_length
    t_w = weld.weld_throat()
    in_plane = weld.in_plane_shear()
    out_of_plane = weld.out_of_plane_shear()
    governing_label = "In-plane" if in_plane >= out_of_plane else "Out-of-plane"
    governing_color = "#b22222"
    in_plane_color = governing_color if governing_label == "In-plane" else "#1f77b4"
    out_of_plane_color = governing_color if governing_label == "Out-of-plane" else "#2a7f62"

    fig, (ax, ax_stress) = plt.subplots(
        1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1.35, 1.0]}
    )

    base_width = max(3.0 * t_p, 5.2 * L_w)
    base_depth = 0.25 * t_p
    web_height = 1.25 * t_p
    web_width = 0.42 * t_p

    for patch in (
        Rectangle((-base_width / 2, -base_depth), base_width, base_depth, fc="#d9d9d9", ec="#555", lw=1.2),
        Rectangle((-web_width / 2, 0), web_width, web_height, fc="#f2f2f2", ec="#555", lw=1.2),
        Polygon([(-web_width / 2, 0), (-web_width / 2 - L_w, 0), (-web_width / 2, L_w)], closed=True, fc="#f7c948", ec="#a66a00", lw=1.2),
        Polygon([(web_width / 2, 0), (web_width / 2 + L_w, 0), (web_width / 2, L_w)], closed=True, fc="#f7c948", ec="#a66a00", lw=1.2),
    ):
        ax.add_patch(patch)

    arrow_y = web_height * 0.72
    ax.annotate("", xy=(base_width * 0.38, arrow_y), xytext=(web_width / 2, arrow_y),
                arrowprops={"arrowstyle": "->", "color": in_plane_color, "lw": 2.2})
    ax.text(base_width * 0.40, arrow_y, "V_ip", color=in_plane_color, fontsize=12, fontweight="bold", va="center")

    oop_center = (-web_width / 2 - 1.25 * L_w, L_w * 0.65)
    ax.add_patch(Circle(oop_center, 0.18 * L_w, fill=False, ec=out_of_plane_color, lw=2.0))
    ax.plot([oop_center[0] - 0.11 * L_w, oop_center[0] + 0.11 * L_w],
            [oop_center[1] - 0.11 * L_w, oop_center[1] + 0.11 * L_w], color=out_of_plane_color, lw=2.0)
    ax.plot([oop_center[0] - 0.11 * L_w, oop_center[0] + 0.11 * L_w],
            [oop_center[1] + 0.11 * L_w, oop_center[1] - 0.11 * L_w], color=out_of_plane_color, lw=2.0)
    ax.text(oop_center[0], oop_center[1] - 0.36 * L_w, "V_oop", color=out_of_plane_color,
            fontsize=12, fontweight="bold", ha="center")

    for x_sign in (1, -1):
        center = (x_sign * (web_width / 2 + 1.35 * L_w), L_w * 0.95)
        radius = 0.55 * L_w
        ax.add_patch(Arc(center, 2 * radius, 2 * radius, theta1=35, theta2=310, color="#f58518", lw=2.0))
        end_angle = math.radians(310)
        end = (center[0] + radius * math.cos(end_angle), center[1] + radius * math.sin(end_angle))
        tangent = (-math.sin(end_angle), math.cos(end_angle))
        ax.annotate("", xy=end,
                    xytext=(end[0] - 0.22 * radius * tangent[0], end[1] - 0.22 * radius * tangent[1]),
                    arrowprops={"arrowstyle": "->", "color": "#f58518", "lw": 2.0})

    ax.annotate("", xy=(web_width / 2 + L_w, -0.08 * t_p), xytext=(web_width / 2, -0.08 * t_p),
                arrowprops={"arrowstyle": "<->", "color": "#333", "lw": 1.2})
    ax.text(web_width / 2 + L_w / 2, -0.16 * t_p, f"L_w = {L_w:.3g} in", ha="center", va="top", fontsize=9)
    ax.text(web_width / 2 + 0.62 * L_w, 0.55 * L_w, f"t_w = {t_w:.3g} in", color="#a66a00", fontsize=9)
    ax.text(base_width / 2 * 0.72, -base_depth / 2, f"t_p = {t_p:.3g} in", color="#333", fontsize=9, va="center")

    ax.set_title("Fillet Weld Load Sketch", fontweight="bold")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-base_width / 2 - 0.12 * base_width, base_width / 2 + 0.18 * base_width)
    ax.set_ylim(-0.40 * t_p, web_height + 0.15 * t_p)
    ax.axis("off")

    verdict = "Demand only" if weld.passes() is None else ("PASS" if weld.passes() else "FAIL")
    verdict_color = "#333" if weld.passes() is None else ("#1b6e1b" if weld.passes() else "#a40000")
    ax_stress.axis("off")
    ax_stress.set_title(f"Weld Stress Table - {verdict}", color=verdict_color, fontweight="bold")

    rows = [
        ["tau_wd", "Direct", f"{weld.shear_from_direct():.1f}", "psi"],
        ["tau_wp", "Plate shear", f"{weld.shear_from_plate_shear():.1f}", "psi"],
        ["tau_wb", "Bending", f"{weld.shear_from_bending():.1f}", "psi"],
        ["V_ip", "In-plane", f"{in_plane:.1f}", "psi"],
        ["V_oop", "Out-of-plane", f"{out_of_plane:.1f}", "psi"],
        ["T_w", "Total", f"{weld.total_shear():.1f}", "psi"],
    ]
    if weld.allowable_stress is not None:
        rows.extend([
            ["T_allow", "Allowable", f"{weld.allowable_stress:.1f}", "psi"],
            ["U", "Utilization", f"{weld.utilization():.1%}", ""],
        ])

    table = ax_stress.table(
        cellText=rows,
        colLabels=["Symbol", "Stress", "Value", "Unit"],
        cellLoc="left",
        colLoc="left",
        colWidths=[0.20, 0.48, 0.22, 0.10],
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1.0, 1.45)

    fig.suptitle(title, fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    weld = FilletWeld(
        plate_thickness=16.0,
        weld_leg_length=6.0,
        plate_direct_stress=50.0,
        plate_shear_stress=25.0,
        plate_bending_stress=60.0,
        allowable_stress=15000.0,
    )
    weld.report()
    plot_fillet_weld(weld)
    import matplotlib.pyplot as plt
    plt.show()
